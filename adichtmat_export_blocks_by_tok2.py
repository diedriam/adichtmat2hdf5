import argparse
from adichtmat import Adichtmatfile
from xtokens import Xtoken, Xtokenset
import os
import sys
from pathlib import Path
from shutil import copyfile


def adichtmat_export_blocks_by_tok(
    filename: str,
    tok_id: str = "",
    tok_longid: str = "",
    tok_start: str = "",
    tok_end: str = "",
    xtoken_def: str = "./conf/xtokens.json",
):
    """export block identified by tok_longid and interval defined by tok_start and tok_end"""
    if tok_longid == "":
        tok_longid = tok_id
    if tok_id == "":
        xtokenset = Xtokenset(filename=xtoken_def)
        xtokenset.load()
        tokens = xtokenset.xtokens
    else:
        tokens = [Xtoken(tok_id, tok_longid, tok_start, tok_end)]
    print(tokens)

    path = os.path.dirname(filename)
    fn_base = os.path.basename(filename)

    ad = Adichtmatfile(filename)
    ad.loadinfo()

    """ get comtab in form of df """
    comtab = ad.get_comments_table()
    df = ad.get_comments_table()

    """ extract NIBP """
    df[["SBP", "DBP", "MBP", "HR"]] = df.comments.str.extract(
        "@NIBP = (\d+) / (\d+) \((\d+)\)\, (\d+)"
    )
    df.drop(columns=["sig_id", "type_id", "text_id", "tick_pos"], inplace=True)

    path = os.path.dirname(ad.filename)
    fn_out = os.path.basename(ad.filename)
    fn_out = "{}_comments_wNIBP.xlsx".format(
        os.path.join(path, os.path.splitext(fn_out)[0])
    )
    print("export comments table {}...".format(fn_out))
    df.to_excel(fn_out, index=False)
    print("export comments table with NIBP done.")

    for tok in tokens:
        # TODO: convert to function for seaching tok in comtab
        tok_id = tok.tok_id
        tok_longid = tok.tok_longid
        tok_start = tok.tok_start
        tok_end = tok.tok_end

        """search main tok id """
        """time info in output filename is derived from main tokid"""
        c = ad.find_comment(tok_longid, searchmode="startswith")

        if c.empty:
            print("block for " + tok_longid + " not found.")
        else:
            """call procedure for each found longid tok """
            """it would be better to put this in function"""
            
            for index, row in c.iterrows():
                #longid_tick = row.tick_pos
                longid_blk = row.blk_id - 1  # we use blk = blk_id -1 counting from 0
                longid_dtm = row.date_time

                """"search for closest start tok before the longid"""
                start_tick = -1
                longid_tick = -1
                if len(tok_start) > 0:
                    a = ad.find_comment(
                        tok_start,
                        longid_blk,
                        to_tick_pos=longid_tick,
                        searchmode="startswith",
                    )
                    if not a.empty:
                        start_tick = a.tick_pos.iloc[-1]

                """search for closest stop tok after the longid"""
                stop_tick = -1
                if len(tok_end) > 0:
                    b = ad.find_comment(
                        tok_end,
                        longid_blk,
                        from_tick_pos=start_tick,
                        searchmode="startswith",
                    )
                    if not b.empty:
                        stop_tick = b.tick_pos.iloc[0]

                fn_root = "{}_blk{}_{}_T{}".format(
                    os.path.splitext(fn_base)[0],
                    longid_blk + 1,
                    tok_id,
                    longid_dtm.strftime("%H%M%S"),
                )
                path_out = os.path.join(path, "cuts")
                if not os.path.isdir(path_out):
                    os.mkdir(path_out)
                path_out = os.path.join(path, "cuts", fn_root)
                if not os.path.isdir(path_out):
                    os.mkdir(path_out)
                print(f"export blk {fn_root}.mat ...")

                tickrate = ad.get_tickrates(longid_blk)
                datalen = max(ad.get_datalen_ticks(None, longid_blk))
                if start_tick > -1:
                    start_tick2 = start_tick-tickrate*120
                    stop_tick2 = start_tick+tickrate*120
                    if start_tick2 > -1:
                        start_tick = start_tick2
                    else: 
                        start_tick = 0
                    if (stop_tick2 > -1) & (stop_tick2 < datalen):
                        stop_tick = stop_tick2
                    else:
                        stop_tick = datalen
                    ad.export_block(
                        longid_blk,
                        start_tick=start_tick,
                        stop_tick=stop_tick,
                        filename=os.path.join(path_out, fn_root + ".mat"),
                    )

                    """ copy pin file if available """
                    fn_pin = os.path.splitext(fn_base)[0] + ".pin"
                    fnfull_pin = os.path.join(path, fn_pin)
                    if os.path.isfile(fnfull_pin):
                        print(f"coping pin file {fn_pin} ...")
                        copyfile(fnfull_pin, os.path.join(path_out, fn_root + ".pin"))
                    else:
                        print(f"pin file {fn_pin} not found.")

    print(f"adichtmat export by tok for {fn_base} done.")


def main(args):
    print(args)
    adichtmat_export_blocks_by_tok(
        args.filename,
        tok_id=args.tok_id,
        tok_longid=args.tok_longid,
        tok_start=args.tok_start,
        tok_end=args.tok_end,
        xtoken_def=args.xtoken_def,
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="view ekf log file")
    parser.add_argument("filename", type=str)
    parser.add_argument("-i", "--tok_id", default="")
    parser.add_argument("-l", "--tok_longid", type=str, default="")
    parser.add_argument("-s", "--tok_start", type=str, default="")
    parser.add_argument("-e", "--tok_end", type=str, default="")
    parser.add_argument("-x", "--xtoken_def", type=str, default="./conf/xtokens.json")
    args = parser.parse_args()
    main(args)
