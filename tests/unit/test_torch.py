


import torch
from serving.core.protocol import serialize_tensor, deserialize_tensor



def test_round_trip():

    for i in range(100):
        t = torch.randn((1, 3, 224, 224))
        assert (deserialize_tensor(serialize_tensor(t)) - t).abs().sum() == 0
