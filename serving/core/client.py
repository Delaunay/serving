from argparse import ArgumentParser
import asyncio
import torch

from serving.core.protocol import model_rpc


async def client():
    parser = ArgumentParser()
    parser.add_argument('--image', default="image.jpeg")
    parser.add_argument('--port', default=8081)
    parser.add_argument('--ip', default='localhost')

    args = parser.parse_args()
    
    reader, writer = await asyncio.open_connection(
        args.ip, 
        args.port
    )

    batch = torch.randn((1, 3, 224, 224))

    output = await model_rpc(reader, writer, batch)
    print(output.shape)

    writer.close()
    await writer.wait_closed()


def main():
    asyncio.run(client())


if __name__ == '__main__':
    for i in range(10000):
        main()
