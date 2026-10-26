#!/usr/bin/env python3
"""逐字节校验 skill/telecom-weekly-analysis/ 与已安装 Skill 源目录是否完全一致。

用法：python3 scripts/verify_skill_export.py <本机已安装Skill目录>
输出：每个文件的 SHA256（源 / 导出）、字节数、比对结果，以及整体结论。
只做只读校验，不修改任何文件。
"""
import hashlib
import pathlib
import sys

if len(sys.argv) != 2:
    raise SystemExit("用法：python3 scripts/verify_skill_export.py <本机已安装Skill目录>")
SRC = pathlib.Path(sys.argv[1]).expanduser().resolve()
if not SRC.is_dir():
    raise SystemExit("源目录不存在")

DST = pathlib.Path(__file__).resolve().parent.parent / "skill" / "telecom-weekly-analysis"

# 安装元数据与用户信息，不导出
EXCLUDE = {"_meta.json"}


def sha256(path: pathlib.Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def main() -> int:
    src_files = sorted(
        p.relative_to(SRC) for p in SRC.rglob("*") if p.is_file() and p.name not in EXCLUDE
    )
    dst_files = sorted(p.relative_to(DST) for p in DST.rglob("*") if p.is_file())

    print(f"源目录  : {SRC}")
    print(f"导出目录: {DST}")
    print(f"源文件数（排除 {sorted(EXCLUDE)}）: {len(src_files)}")
    print(f"导出文件数: {len(dst_files)}")
    print()

    extra = [str(f) for f in dst_files if f not in src_files]
    missing = [str(f) for f in src_files if f not in dst_files]
    ok = True

    print("| 文件 | 字节 | SHA256（源） | SHA256（导出） | 结果 |")
    for rel in src_files:
        s = SRC / rel
        d = DST / rel
        hs = sha256(s)
        if d.exists():
            hd = sha256(d)
        else:
            hd = "-"
        same = hs == hd
        ok = ok and same
        print(
            f"| {rel.as_posix()} | {s.stat().st_size} | {hs} | {hd} | "
            f"{'一致' if same else '不一致'} |"
        )

    print()
    print(f"缺失文件: {missing if missing else '无'}")
    print(f"多余文件: {extra if extra else '无'}")
    print(f"整体结论: {'全部逐字节一致' if ok and not missing and not extra else '存在差异，需人工复核'}")
    return 0 if ok and not missing and not extra else 1


if __name__ == "__main__":
    sys.exit(main())
