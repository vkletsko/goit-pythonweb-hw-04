import argparse
import asyncio
import logging as log
from aiopath import AsyncPath
from aioshutil import copyfile

log.basicConfig(level=log.INFO)


async def copy_file(source_path: AsyncPath, output_dir: AsyncPath):
    try:
        extension = source_path.suffix.lower()
        output_subdir = output_dir / extension.strip('.')
        await output_subdir.mkdir(parents=True, exist_ok=True)
        dest_file = output_subdir / source_path.name
        await copyfile(source_path, dest_file)
        log.info(f'File {source_path.name} copied to {output_subdir}')
    except Exception as e:
        log.error(f"Copying error of {source_path} to {output_subdir}: {e}")


async def read_folder(source_dir: AsyncPath, dest_dir: AsyncPath):
    tasks = []
    async for path in source_dir.rglob('*'):
        if await path.is_file():
            tasks.append(copy_file(path, dest_dir))
    await asyncio.gather(*tasks)


def main():
    parser = argparse.ArgumentParser(description='Async copying and organising files from Source to Output folders')
    parser.add_argument('source', help='Source folder')
    parser.add_argument('destination', help='Output folder')
    args = parser.parse_args()

    source_dir = AsyncPath(args.source)
    dest_dir = AsyncPath(args.destination)

    asyncio.run(read_folder(source_dir, dest_dir))


if __name__ == '__main__':
    main()
