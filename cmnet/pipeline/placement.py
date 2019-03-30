# Wrapper for placement tools

from subprocess import check_call
import os
from os import path
from pathlib import Path

from cmnet.utils import make_output_dir, read_stockholm, read_fasta, write_fasta


# Phylogenetic madness
#
#

def seq_placement(study_fasta:str,
                  ref_msa:str,
                  ref_tree:str,
                  hmm:str,
                  out_tree:str,
                  threads:int,
                  out_dir,
                  chunk_size):
    """ Place sequence on to reference phylogenetic tree

    Align FASTA to ref_msa (which is the one that used to construct tree)


    Args:
        study_fasta:
        ref_msa:
        ref_tree:
        hmm:
        out_tree:
        alignment_tool:
        threads:
        out_dir:
        chunk_size:
    """

    out_stockholm = os.path.join(out_dir, "query_align.stockholm")  # output from hmmalign
    epa_out_dir = path.join(out_dir, "epa_out")
    # Alignment with pre-aligned dataset using hmmaligned.
    run_command = ["hmmalign", "--trim", "--dna", "--mapali", ref_msa, "--informat", "FASTA", "-o",
                out_stockholm, hmm, study_fasta]
    check_call(run_command)
    # Separate alignment file into query and reference.
    study_msa_fastafile = path.join(out_dir, "study_seqs_hmmalign.fasta")
    ref_msa_fastafile = path.join(out_dir, "ref_seqs_hmmalign.fasta")
    # Read all inputs
    hmmalignseqs = read_stockholm(out_stockholm)
    study_subset = read_fasta(study_fasta).keys()
    ref_subset = read_fasta(ref_msa).keys()
    #  Get only fasta of those within study/ref and write it
    study_hmmalign_subset = {name:hmmalignseqs[name] for name in study_subset}
    ref_hmmalign_subset = {name:hmmalignseqs[name] for name in ref_subset}
    write_fasta(study_hmmalign_subset, study_msa_fastafile)
    write_fasta(ref_hmmalign_subset, ref_msa_fastafile)
    # Run epa_ng to impute tree's location
    run_epa_ng(ref_tree=ref_tree, ref_msa_fastafile=ref_msa_fastafile,
               study_msa_fastafile=study_msa_fastafile, chunk_size=chunk_size,
               threads=threads, out_dir=epa_out_dir)
    jplace_outfile = path.join(epa_out_dir, "epa_result.jplace")
    # Then convert into newick for later use.
    gappa_jplace_to_newick(jplace_file=jplace_outfile, outfile=out_tree)


def run_epa_ng(ref_tree: str,
               ref_msa_fastafile: str,
               study_msa_fastafile: str,
               out_dir: str,
               chunk_size=5000,
               threads=1):
    '''Run EPA-NG on specified tree, reference MSA, and study sequence MSA.
    Will opath.joinutput a .jplace file in out_dir.'''

    make_output_dir(out_dir)
    try:
        check_call(["epa-ng", "--bfast", study_msa_fastafile, "--outdir", out_dir])
        study_msa_bfast = path.join(out_dir, path.basename(study_msa_fastafile) +
                                    ".bfast")
        check_call(["epa-ng", "--tree", ref_tree, "--ref-msa", ref_msa_fastafile,
                    "--query", study_msa_bfast, "--chunk-size", str(chunk_size),
                    "-T", str(threads), "-m", "GTR+G", "-w", out_dir])
    except:
        pass # Ok, decide what to do next time


def gappa_jplace_to_newick(jplace_file: str, outfile: str):
    '''System call to gappa binary to convert jplace object to newick
    treefile (with specified filename).'''

    gappa_out_dir = path.dirname(outfile)

    # Run gappa to convert jplace to newick.
    check_call(["gappa", "analyze", "graft", "--jplace-path", jplace_file,
                "--fully-resolve", "--out-dir", gappa_out_dir])

    # Expected name of output newick file.
    newick_file = str(os.path.join(gappa_out_dir, os.path.basename(jplace_file))).replace(".jplace", ".newick")
    os.rename(newick_file, outfile)

#
# End of the phylogenetic madness
#