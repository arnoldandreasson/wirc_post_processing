#!/usr/bin/python3

import asyncio
import src.core as core


async def main():
    """ """
    engine = core.WorkflowEngine()
    await engine.startup("workflow_test.yaml")


if __name__ == "__main__":
    """ """
    asyncio.run(main())
