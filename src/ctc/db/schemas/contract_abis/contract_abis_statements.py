from __future__ import annotations

import json
import typing

import toolsql

from ctc import spec
from ... import schema_utils


async def async_upsert_contract_abi(
    address: spec.Address,
    abi: spec.ContractABI,
    includes_proxy: bool,
    conn: toolsql.SAConnection,
    network: spec.NetworkReference | None = None,
) -> None:

    abi_text = json.dumps(abi)

    table = schema_utils.get_table_name(
        'contract_abis', network=network
    )
    toolsql.insert(
        conn=conn,
        table=table,
        row={
            'address': address.lower(),
            'abi_text': abi_text,
            'includes_proxy': includes_proxy,
        },
        upsert='do_update',
    )


async def async_select_contract_abi(
    address: spec.Address,
    network: spec.NetworkReference | None = None,
    *,
    conn: toolsql.SAConnection,
) -> spec.ContractABI | None:

    table = schema_utils.get_table_name(
        'contract_abis',
        network=network,
    )
    abi_text = toolsql.select(
        conn=conn,
        table=table,
        row_id=address.lower(),
        return_count='one',
        only_columns=['abi_text'],
        row_format='only_column',
    )
    if abi_text is not None:
        return json.loads(abi_text)
    else:
        return None


async def async_select_contract_abis(
    network: spec.NetworkReference | None = None,
    *,
    conn: toolsql.SAConnection,
) -> typing.Mapping[spec.Address, spec.ContractABI]:

    table = schema_utils.get_table_name(
        'contract_abis',
        network=network,
    )

    results = toolsql.select(
        conn=conn,
        table=table,
    )

    return {
        result['address']: json.loads(result['abi_text'])
        for result in results
    }


async def async_delete_contract_abi(
    conn: toolsql.SAConnection,
    address: spec.Address,
    network: spec.NetworkReference | None = None,
) -> None:
    table = schema_utils.get_table_name(
        'contract_abis',
        network=network,
    )
    toolsql.delete(
        conn=conn,
        table=table,
        row_id=address.lower(),
    )