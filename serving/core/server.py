


from argparse import ArgumentParser
import asyncio
from contextlib import contextmanager
import time
from typing import Any

import torch

from serving.core.protocol import read_message, send_message, serialize_tensor, deserialize_tensor


@contextmanager
def timeit(name):

    s = time.time()
    yield 
    t = time.time() - s
    print(f'{name}: {t:.2f}s')


class ModelAdapter:
    def __init__(self, model, device) -> None:
        self.device = device
        self.model = model.to(device=self.device)

    def __call__(self, msg) -> Any:
        with torch.no_grad():
            input = deserialize_tensor(msg).to(device=self.device)
            output = self.model(input)
            return serialize_tensor(output)


def load_model(name, weights):
    from torchvision.models import resnet50, ResNet50_Weights
    
    model = resnet50(weights=ResNet50_Weights.IMAGENET1K_V2)
    return ModelAdapter(model, torch.device("cuda:0"))


async def server():
    parser = ArgumentParser()
    parser.add_argument('model', default='resnet50')
    parser.add_argument('--weights', default="~/.cache")
    parser.add_argument('--port', default=8081)
    parser.add_argument('--ip', default='localhost')
    
    args = parser.parse_args()
    
    # Init
    with timeit("Loading model"):
        model = load_model(args.model, args.weights)

    print(f'Running: {args.ip}:{args.port}')

    # Handler
    async def handle_client(reader, writer):
        
        with timeit("handling request"):
            msg_bytes = await read_message(reader)

            output_bytes = model(msg_bytes)

            await send_message(writer, output_bytes)

            writer.close()
            await writer.wait_closed()

    # Server
    server = await asyncio.start_server(
        handle_client,
        args.ip, 
        args.port
    )

    async with server:
        await server.serve_forever()


def main():
    asyncio.run(server())


if __name__ == '__main__':
    main()
