from __future__ import annotations

import asyncio
import time
import typing
from typing_extensions import TypedDict

from ctc import binary
from ctc import rpc
from ctc import spec


async def async_get_block(
    block: spec.BlockReference,
    include_full_transactions: bool = False,
    provider: spec.ProviderSpec = None,
) -> spec.Block:

    if spec.is_block_number_reference(block):

        block_data = await rpc.async_eth_get_block_by_number(
            block_number=binary.standardize_block_number(block),
            provider=provider,
            include_full_transactions=include_full_transactions,
        )

        from ctc import db

        await db.async_intake_block(
            block=block_data,
            network=rpc.get_provider_network(provider),
        )

        return block_data

    elif spec.is_block_hash(block):

        return await rpc.async_eth_get_block_by_hash(
            block_hash=block,
            provider=provider,
            include_full_transactions=include_full_transactions,
        )

    else:
        raise Exception('unknown block specifier: ' + str(block))


async def async_get_blocks(
    blocks: typing.Sequence[spec.BlockReference],
    include_full_transactions: bool = False,
    chunk_size: int = 500,
    provider: spec.ProviderSpec = None,
) -> list[spec.Block]:

    provider = rpc.add_provider_parameters(provider, {'chunk_size': chunk_size})

    if all(spec.is_block_number_reference(block) for block in blocks):

        standardized = [
            binary.standardize_block_number(block) for block in blocks
        ]

        blocks_data = await rpc.async_batch_eth_get_block_by_number(
            block_numbers=standardized,
            include_full_transactions=include_full_transactions,
            provider=provider,
        )

        from ctc import db

        await db.async_intake_blocks(
            blocks=blocks_data,
            network=rpc.get_provider_network(provider),
        )

        return blocks_data

    elif all(spec.is_block_hash(block) for block in blocks):

        return await rpc.async_batch_eth_get_block_by_hash(
            block_hashes=blocks,
            include_full_transactions=include_full_transactions,
            provider=provider,
        )

    else:
        raise Exception(
            'blocks should be all block number references or all block hashes'
        )


class LatestBlockCacheEntry(TypedDict, total=False):
    request_time: float
    response_time: float
    block_number: int


_latest_block_cache: typing.MutableMapping[str, LatestBlockCacheEntry] = {}
_latest_block_lock = asyncio.Lock()


async def async_get_latest_block_number(
    provider: spec.ProviderSpec = None,
    use_cache: bool = True,
    cache_time: int | float = 1,
) -> int:

    if not use_cache:
        return await rpc.async_eth_block_number(provider=provider)

    else:

        async with _latest_block_lock:

            network = rpc.get_provider_network(provider)
            request_time = time.time()
            network_cache = _latest_block_cache.get(network)
            if (
                network_cache is not None
                and request_time - network_cache['request_time'] < cache_time
            ):
                return network_cache['block_number']

            result = await rpc.async_eth_block_number(provider=provider)

            response_time = time.time()
            _latest_block_cache[network] = {
                'request_time': request_time,
                'response_time': response_time,
                'block_number': result,
            }

            return result
