from q_learning import QLearning


class QLearningAgent:
  def __init__(self, config):
    self.config=config
    self.agent = QLearning(config["train"])
    self.solve_check_behaviour_agent()

  def solve_check_behaviour_agent(self):
    """
     Comunica el comportamiento que ha de seguir el agente; si un proceso de entrenamiento
     o el uso del historial para jugar por si mismo
    """
    if self.agent.train:
      print("Training agent...")
    else:
      print("Running agent...")

  def save_when_is_quit(self):
    self.agent.save_qvalues()
    self.agent.save_training_states()

  def should_be_act(self,bird_pos_x, bird_pos_y, bird_vel_y, lower_pipes_position):
    """
    Evalúa si se debe efectuar un aleteo o no
    :param bird_pos_x: Posición en x del ave
    :param bird_pos_y: Posición en y del ave
    :param bird_vel_y: Velocidad en y del ave
    :param lower_pipes_position: Conjunto de pipes (posiciones inferiores)
    :return:
    """
    return self.agent.act(bird_pos_x, bird_pos_y, bird_vel_y, lower_pipes_position)
