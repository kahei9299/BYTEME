import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import numpy as np

class SimpleTikTokAnalyzer(nn.Module):
    def __init__(self, input_dim, hidden_dim=64):
        super().__init__()
        
        # Simple neural network
        self.network = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(hidden_dim, 5)  # 5 output scores
        )
        
    def forward(self, x):
        return self.network(x)

class TikTokModelTrainer:
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        
    def prepare_data(self, features, scores):
        """Prepare data for training"""
        # Normalize features
        X = self.scaler.fit_transform(features)
        y = np.array(scores)
        
        # Check if we have enough data for train/test split
        if len(X) < 2:
            # If only 1 sample, use it for both training and testing
            print("⚠️  Only 1 video in dataset - using it for both training and testing")
            return X, X, y, y
        elif len(X) < 5:
            # If less than 5 samples, use smaller test size
            test_size = 0.1  # 10% for testing
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=test_size, random_state=42
            )
        else:
            # Normal split for larger datasets
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42
            )
        
        return X_train, X_test, y_train, y_test
    
    def train(self, X_train, y_train, epochs=100):
        """Train the model"""
        input_dim = X_train.shape[1]
        self.model = SimpleTikTokAnalyzer(input_dim)
        
        # Convert to PyTorch tensors
        X_train_tensor = torch.FloatTensor(X_train)
        y_train_tensor = torch.FloatTensor(y_train)
        
        # Loss and optimizer
        criterion = nn.MSELoss()
        optimizer = optim.Adam(self.model.parameters(), lr=0.001)
        
        # Training loop
        for epoch in range(epochs):
            optimizer.zero_grad()
            outputs = self.model(X_train_tensor)
            loss = criterion(outputs, y_train_tensor)
            loss.backward()
            optimizer.step()
            
            if epoch % 10 == 0:
                print(f'Epoch {epoch}, Loss: {loss.item():.4f}')
    
    def predict(self, X):
        """Make predictions"""
        if self.model is None:
            raise ValueError("Model not trained yet")
        
        X_scaled = self.scaler.transform(X)
        X_tensor = torch.FloatTensor(X_scaled)
        
        self.model.eval()
        with torch.no_grad():
            predictions = self.model(X_tensor)
        
        return predictions.numpy()
    
    def evaluate(self, X_test, y_test):
        """Evaluate model performance"""
        predictions = self.predict(X_test)
        
        # Calculate metrics for each score
        metrics = {}
        score_names = ['accuracy', 'homogeneity', 'comedy', 'theatrism', 'coherence']
        
        for i, name in enumerate(score_names):
            mse = np.mean((y_test[:, i] - predictions[:, i]) ** 2)
            mae = np.mean(np.abs(y_test[:, i] - predictions[:, i]))
            metrics[name] = {'mse': mse, 'mae': mae}
        
        return metrics

# Example usage
if __name__ == "__main__":
    # This will be used when you have data
    trainer = TikTokModelTrainer()
    print("Model trainer created successfully!")