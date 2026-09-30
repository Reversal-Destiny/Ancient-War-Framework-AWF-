# Third-party notices

## QuModLibs

AWF v0.1.0 selectively derives and rewrites framework mechanisms from **QuModLibs v1.4** by Zero123, including the conceptual shape of decorator-based native event registration, RPC-call registration/sender injection, and a single loader/root-system lifecycle.

QuModLibs repository: `https://github.com/GitHub-Zero123/QuModLibs`

The files containing the most direct derivative design are marked in source comments, especially:

- `Core/Event/Decorators.py`
- `Core/RPC/Decorators.py`
- `Bootstrap/ServerSystem.py`
- RPC/event bootstrap behavior in `Core/RPC/RPCManager.py`

QuModLibs is distributed under the BSD 3-Clause License. The retained license text is in `licenses/QuModLibs-BSD-3-Clause.txt`.

AWF deliberately does **not** retain QuModLibs' import-side-effect initialization model. Feature loading, dependency resolution, service registration, registry freezing and endpoint registration are explicit in AWF.
