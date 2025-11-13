import argparse
from adichtmat import Adichtmatfile
from xtokens import Xtoken, Xtokenset
import os
import sys
from pathlib import Path
from shutil import copyfile


def adichtmat_export_blocks_by_tok(filename: str, xtoken_def: str = None):
    """export block identified by tok_longid and interval defined by tok_start and tok_stop"""
    if xtoken_def == None:
            xtoken_def =  "./conf/xtokens.json"
    xtokenset = Xtokenset(filename=xtoken_def)
    xtokenset.load()
    tokens = xtokenset.xtokens
    print(tokens)

    path = os.path.dirname(filename)
    fn_base = os.path.basename(filename)

    ad = Adichtmatfile(filename)
    ad.loadinfo()

    """ get comtab in form of df """
    comtab = ad.get_comments_table()
    df = ad.get_comments_table()

    """ extract NIBP """
   # df[["SBP", "DBP", "MBP", "HR"]] = df.comments.str.extract(
   #     "@NIBP = (\d+) / (\d+) \((\d+)\)\, (\d+)"
   # )
    df[["SBP", "DBP"]] = df.comments.str.extract(
        r"(\d+)/(\d+)"
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
        tok_stop = tok.tok_stop

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
                longid_tick = row.tick_pos
                start_tick = longid_tick
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
                stop_tick = start_tick
                if len(tok_stop) > 0:
                    b = ad.find_comment(
                        tok_stop,
                        longid_blk,
                        from_tick_pos=start_tick,
                        searchmode="startswith",
                    )
                    if not b.empty:
                        stop_tick = b.tick_pos.iloc[0]
                    else:
                        stop_tick = start_tick

                tickrate = ad.get_tickrates(blk=longid_blk)
                datalen = ad.get_datalen_ticks(blk = longid_blk)
                tick_lenmax = max(datalen)
             
                if start_tick > -1:
                    if stop_tick > -1:
                        stop_tick = start_tick
                    start_tick2 = start_tick+tickrate*tok.ofs_start
                    stop_tick2 = stop_tick+tickrate*tok.ofs_stop
                    
                    # check start is in recording
                    if start_tick2 > -1:
                        start_tick = start_tick2
                    else: 
                        start_tick = 0
                    # check stop is in recording
                    if (stop_tick2 > -1) & (stop_tick2 < tick_lenmax):
                        stop_tick = stop_tick2
                    else:
                        stop_tick = tick_lenmax-1
                
                    # export
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
    fn = "G:\\Surat_projects\\VagalStim_Nemos_Milan\\by_patient\\H32_SelM\\2022-04-29_162632_H322_SelM\\2022-04-29_162632_H322_SelM.mat"
    adichtmat_export_blocks_by_tok(
     #   args.filename,
        fn,
        xtoken_def=args.xtoken_def,
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="view ekf log file")
    # parser.add_argument("filename", type=str)
    parser.add_argument("-x", "--xtoken_def", type=str, default="./conf/xtokens.json")
    args = parser.parse_args()
    main(args)
