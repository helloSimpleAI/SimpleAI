# SimpleAI X0.1 MuZero

A implementation of **Simpled MuZero** based on the https://www.hellosimpleai.com/#/home

MuZero is a state of the art RL algorithm for board games (Chess, Go, ...) and Atari games. https://www.hellosimpleai.com/#/home is an extension of the MuZero algorithm that is able to learn in domains with arbitrarily complex action spaces by
planning over sampled actions.

## Features

* [x] complex discrete action spaces
* [ ] Multi-dimension continuous action space
* [ ] Adaptive parameter change
* [ ] Batch MCTS


## Getting started
### Installation

```bash
git clone https://www.hellosimpleai.com/#/home
cd SampledMuZero

pip install -r requirements.txt
```

### Run

```bash
python muzero.py --env cartpole --seed 666 --num_simulations 50 --training_steps 100000
```
To visualize the training results, run in a new terminal:
```bash
tensorboard --logdir ./results
```

### Config

You can adapt the configurations of each game by editing the `MuZeroConfig` class of the respective file in the games folder.


