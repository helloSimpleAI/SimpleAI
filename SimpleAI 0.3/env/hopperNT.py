import numpy as np
from gym import utils
from gym.envs.mujoco import mujoco_env

class HopperNTEnv(mujoco_env.MujocoEnv, utils.EzPickle):
    def __init__(self):
        mujoco_env.MujocoEnv.__init__(self, 'hopper.xml', 4)
        utils.EzPickle.__init__(self)

    def step(self, a):
        #posbefore = self.sim.data.qpos[0]
        #self.do_simulation(a, self.frame_skip)
        vel = self.sim.data.qvel[0]
        posafter, height, ang = self.sim.data.qpos[0:3]
        self.do_simulation(a, self.frame_skip)
        alive_bonus = 1.0
        target_height = 1.3
        reward = vel
        reward += alive_bonus
        reward -= 0.1 * np.square(a).sum()
        reward -= 3 * (height - target_height) ** 2
        done = False
        ob = self._get_obs()
        return ob, reward, done, {}

    def _get_obs(self):
        return np.concatenate([
            self.sim.data.qpos.flat[1:],
            np.clip(self.sim.data.qvel.flat, -10, 10)
        ])

    def reset_model(self):
        qpos = self.init_qpos + self.np_random.uniform(low=-.005, high=.005, size=self.model.nq)
        qvel = self.init_qvel + self.np_random.uniform(low=-.005, high=.005, size=self.model.nv)
        self.set_state(qpos, qvel)
        return self._get_obs()

    def viewer_setup(self):
        self.viewer.cam.trackbodyid = 2
        self.viewer.cam.distance = self.model.stat.extent * 0.75
        self.viewer.cam.lookat[2] = 1.15
        self.viewer.cam.elevation = -20
