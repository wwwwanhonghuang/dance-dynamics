import torch
import torch.nn as nn
import torch.optim as optim
from torchdiffeq import odeint
import numpy as np
import matplotlib.pyplot as plt

# Set device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
torch.set_default_dtype(torch.float64)

class DanceDynamicsModel(nn.Module):
    def __init__(self, num_dancers, feature_dim, hidden_dim=64):
        super().__init__()
        self.num_dancers = num_dancers
        self.feature_dim = feature_dim
        self.hilbert_dim = 2 ** num_dancers  # Using qubit representation
        
        # Hamiltonian parameters (Hermitian)
        self.H_self = nn.Parameter(torch.randn(num_dancers, feature_dim, feature_dim))
        self.H_coupling = nn.Parameter(torch.randn(num_dancers, num_dancers, feature_dim, feature_dim))
        
        # Lindblad operators (non-Hermitian processes)
        self.lindblad_rates = nn.Parameter(torch.randn(num_dancers, num_dancers, feature_dim, feature_dim))
        
        # Initial state parameters
        self.rho_0 = nn.Parameter(torch.eye(self.hilbert_dim, requires_grad=True))
        
        # Neural network to map features to quantum operators
        self.feature_to_operator = nn.Sequential(
            nn.Linear(feature_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, feature_dim * feature_dim)
        )
        
    def hamiltonian(self, features):
        """Construct the Hamiltonian from current features"""
        # Self-energy terms
        H = torch.zeros(self.hilbert_dim, self.hilbert_dim, device=device)
        
        for i in range(self.num_dancers):
            # Get operator for this dancer's features
            op_i = self.feature_to_operator(features[i]).view(self.feature_dim, self.feature_dim)
            H_i = op_i @ self.H_self[i] + self.H_self[i].conj().T @ op_i.conj().T
            
            # Embed in full Hilbert space
            H += torch.kron(torch.kron(torch.eye(2**i, device=device), 
                                     H_i),
                           torch.eye(2**(self.num_dancers-i-1), device=device))
        
        # Interaction terms
        for i in range(self.num_dancers):
            for j in range(i+1, self.num_dancers):
                # Get operators for both dancers
                op_i = self.feature_to_operator(features[i]).view(self.feature_dim, self.feature_dim)
                op_j = self.feature_to_operator(features[j]).view(self.feature_dim, self.feature_dim)
                
                H_ij = torch.kron(op_i, op_j) @ self.H_coupling[i, j] + self.H_coupling[i, j].conj().T @ torch.kron(op_i.conj().T, op_j.conj().T)
                
                # Embed in full Hilbert space
                left = torch.eye(2**i, device=device)
                middle = torch.kron(H_ij, torch.eye(2**(self.num_dancers-j-1), device=device))
                right = torch.eye(2**(self.num_dancers-i-1), device=device)
                
                H += torch.kron(torch.kron(left, middle), right)
        
        return H
    
    def lindblad_operators(self, features):
        """Construct Lindblad operators from current features"""
        L_ops = []
        
        for i in range(self.num_dancers):
            for j in range(self.num_dancers):
                if i == j:
                    # Single-dancer processes
                    op_i = self.feature_to_operator(features[i]).view(self.feature_dim, self.feature_dim)
                    L = torch.sqrt(torch.abs(self.lindblad_rates[i, j])) * op_i
                    L_ops.append(L)
                else:
                    # Correlated processes between dancers
                    op_i = self.feature_to_operator(features[i]).view(self.feature_dim, self.feature_dim)
                    op_j = self.feature_to_operator(features[j]).view(self.feature_dim, self.feature_dim)
                    L = torch.sqrt(torch.abs(self.lindblad_rates[i, j])) * torch.kron(op_i, op_j)
                    L_ops.append(L)
        
        return L_ops
    
    def lindblad_equation(self, t, rho_flat):
        """The Lindblad master equation"""
        # Reshape from flattened to matrix
        rho = rho_flat.view(self.hilbert_dim, self.hilbert_dim)
        
        # Get current features (in a real application, we'd interpolate from data)
        # For simplicity, we assume features are constant during integration
        features = self.current_features
        
        # Hamiltonian part
        H = self.hamiltonian(features)
        commutator_H = -1j * (H @ rho - rho @ H)
        
        # Lindblad (dissipative) part
        L_ops = self.lindblad_operators(features)
        dissipator = torch.zeros_like(rho)
        
        for L in L_ops:
            L_dag = L.conj().T
            dissipator += L @ rho @ L_dag - 0.5 * (L_dag @ L @ rho + rho @ L_dag @ L)
        
        # Total derivative
        drho_dt = commutator_H + dissipator
        
        # Flatten for ODE solver
        return drho_dt.view(-1)
    
    def forward(self, features, t_eval):
        """Solve the Lindblad equation for given features and time points"""
        self.current_features = features
        
        # Initial state
        rho_0_flat = self.rho_0.view(-1)
        
        # Solve the ODE
        solution = odeint(self.lindblad_equation, rho_0_flat, t_eval, method='dopri5')
        
        # Reshape solution to density matrices
        return solution.view(-1, self.hilbert_dim, self.hilbert_dim)

def quantum_fidelity(rho, sigma):
    """Calculate quantum fidelity between two density matrices"""
    sqrt_rho = torch.matrix_exp(0.5 * torch.log(rho + 1e-12))
    fidelity = torch.trace(sqrt_rho @ sigma @ sqrt_rho).real
    return torch.sqrt(fidelity + 1e-12)

def create_synthetic_data(num_timesteps, num_dancers, feature_dim):
    """Create synthetic dance data for testing"""
    # Random features that evolve smoothly over time
    time = torch.linspace(0, 10, num_timesteps)
    features = torch.zeros(num_timesteps, num_dancers, feature_dim)
    
    for i in range(num_dancers):
        for j in range(feature_dim):
            # Create smooth random motion for each feature
            freq = torch.randn(1).abs() * 2
            phase = torch.randn(1) * 2 * np.pi
            amp = torch.randn(1).abs()
            
            features[:, i, j] = amp * torch.sin(freq * time + phase)
    
    # Create target density matrices (in a real application, these would come from data)
    targets = torch.eye(2 ** num_dancers).unsqueeze(0).repeat(num_timesteps, 1, 1)
    
    return time, features, targets

def train_model():
    # Hyperparameters
    num_dancers = 2
    feature_dim = 3
    num_timesteps = 100
    epochs = 500
    learning_rate = 0.01
    
    # Create model
    model = DanceDynamicsModel(num_dancers, feature_dim).to(device)
    
    # Create synthetic data
    time, features, targets = create_synthetic_data(num_timesteps, num_dancers, feature_dim)
    time = time.to(device)
    features = features.to(device)
    targets = targets.to(device)
    
    # Optimizer
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)
    
    # Training loop
    losses = []
    for epoch in range(epochs):
        optimizer.zero_grad()
        
        # Forward pass: solve Lindblad equation
        predictions = model(features, time)
        
        # Calculate loss (quantum fidelity)
        loss = 0
        for t in range(num_timesteps):
            loss += 1 - quantum_fidelity(predictions[t], targets[t])
        loss = loss / num_timesteps
        
        # Backward pass
        loss.backward()
        optimizer.step()
        
        losses.append(loss.item())
        
        if epoch % 50 == 0:
            print(f"Epoch {epoch}, Loss: {loss.item():.6f}")
    
    # Plot training loss
    plt.figure(figsize=(10, 5))
    plt.plot(losses)
    plt.xlabel("Epoch")
    plt.ylabel("Loss")
    plt.title("Training Loss")
    plt.yscale("log")
    plt.show()
    
    return model

# Train the model
model = train_model()