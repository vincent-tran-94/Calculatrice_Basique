import torch.nn as nn

"""
Réseau neurones artificielles 

Cette méthode définit le passage avant du réseau. Elle prend une entrée x et la fait passer à travers 
chaque couche linéaire suivie d'une fonction d'activation ReLU. L'activation ReLU (self.relu) est appliquée 
après chaque couche linéaire. La sortie de la dernière couche linéaire (self.l3) est renvoyée sans application
d'une activation finale ou d'un softmax. Cela peut indiquer que ce modèle est utilisé pour une tâche de régression ou que 
l'activation et le softmax seront gérés à l'extérieur du modèle, selon l'utilisation prévue.

En résumé, ce script définit une architecture simple de réseau de neurones avec trois couches linéaires et des 
activations ReLU entre elles. Ce modèle peut être utilisé pour différentes tâches en fonction des paramètres input_size, 
hidden_size, et num_classes fournis lors de l'initialisation.
"""
class NeuralNet(nn.Module):
    def __init__(self, input_size, hidden_size, num_classes):
        super(NeuralNet, self).__init__()
        self.l1 = nn.Linear(input_size, hidden_size) 
        self.l2 = nn.Linear(hidden_size, hidden_size) 
        self.l3 = nn.Linear(hidden_size, num_classes)
        self.relu = nn.ReLU()
    
    def forward(self, x):
        out = self.l1(x)
        out = self.relu(out)
        out = self.l2(out)
        out = self.relu(out)
        out = self.l3(out)
        # no activation and no softmax at the end
        return out
