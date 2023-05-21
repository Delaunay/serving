import io
from struct import unpack
import torch


async def read_message(reader):
    # <msg len>.<msg>
    msg_len_bytes = await reader.read(4)
    msg_len = int(unpack("@I", msg_len_bytes)[0])
    msg_bytes = await reader.readexactly(msg_len)

    return msg_bytes


async def model_rpc(reader, writer, inputs):
    inbytes = serialize_tensor(inputs)
    await send_message(writer, inbytes)

    outbytes = await read_message(reader)
    return deserialize_tensor(outbytes)


async def send_message(writer, message):
    # <msg len>.<msg>
    output_len = len(message)
    output_len_bytes = output_len.to_bytes(4, 'little')

    writer.write(output_len_bytes)
    writer.write(message)

    await writer.drain()


def serialize_tensor(msg):
    buff = io.BytesIO()
    torch.save(msg.cpu(), buff)
    return buff.getvalue()


def deserialize_tensor(msg):
    b = io.BytesIO(msg)
    return torch.load(b)