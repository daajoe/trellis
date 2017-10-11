from trellis.decomposer.pace import PACEDecomposer


# TODO: Jdrasil heuristic
# -heuristic

class Jdrasil2016(PACEDecomposer):
    name = 'jdrasil2016'
    bin_name = 'jdrasil'
    folder_name = 'jdrasil2016'

    args = ['-log -e PBLib_incremental', '-log -e commander', '-log -e PBLib']

class Jdrasil2017(PACEDecomposer):
    name = 'jdrasil2017'
    bin_name = 'jdrasil'
    folder_name = 'jdrasil2017'

    #TODO:
    args = ['-log -e PBLib_incremental', '-log -e commander', '-log -e PBLib']


#tw-exact-parallel
#tw-heuristic
#tw-heuristic-parallel