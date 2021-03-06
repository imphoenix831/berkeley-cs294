from utils import parse_args

from distutils.util import strtobool

import numpy as np
import tensorflow as tf
import gym

import models
import agents

def get_available_gpus():
    from tensorflow.python.client import device_lib
    local_device_protos = device_lib.list_local_devices()
    available_gpus = [
        device_proto.physical_device_desc
        for device_proto in local_device_protos
        if device_proto.device_type == 'GPU'
    ]
    return available_gpus


def get_session():
    tf.reset_default_graph()
    tf_config = tf.ConfigProto(
        inter_op_parallelism_threads=1,
        intra_op_parallelism_threads=1
    )
    session = tf.Session(config=tf_config)
    print("AVAILABLE GPUS: ", get_available_gpus())
    return session


def main():
    args = parse_args()

    seed = 0
    env_name = args['env']
    # env = gym.make(args['env'])
    # TODO: set seeds

    session = get_session()
    max_timesteps = args['max_timesteps'] or env.spec.timestep_limit

    ActorCritic = getattr(models, args['ac_model'])

    AgentCls = getattr(agents, args['agent'])
    agent_config = agents.DEFAULT_AGENT_CONFIG.copy()

    ModelCls = getattr(models, args['ac_model'])
    model_config = models.DEFAULT_MODEL_CONFIG.copy()

    Agent = AgentCls(env_name, ModelCls, agent_config, model_config)

    Agent.learn()


if __name__ == "__main__":
    main()
