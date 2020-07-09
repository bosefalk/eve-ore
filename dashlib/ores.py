import ore_value as ore
import pandas as pd
import numpy as np

def ore_df():
    kern_norm_sell = ore.sell_kernite(volume=10000, unit="m3", type="N")
    kern_fire_sell = ore.sell_kernite(volume=10000, unit="m3", type="F")
    kern_lum_sell = ore.sell_kernite(volume=10000, unit="m3", type="L")
    kern_norm_rep = ore.rep_kernite(volume=10000, unit="m3", type="N")
    kern_fire_rep = ore.rep_kernite(volume=10000, unit="m3", type="F")
    kern_lum_rep = ore.rep_kernite(volume=10000, unit="m3", type="L")
    pyro_norm_sell = ore.sell_pyro(volume=10000, unit="m3", type="N")
    pyro_solid_sell = ore.sell_pyro(volume=10000, unit="m3", type="S")
    pyro_visc_sell = ore.sell_pyro(volume=10000, unit="m3", type="V")
    pyro_norm_rep = ore.rep_pyro(volume=10000, unit="m3", type="N")
    pyro_solid_rep = ore.rep_pyro(volume=10000, unit="m3", type="S")
    pyro_visc_rep = ore.rep_pyro(volume=10000, unit="m3", type="V")
    veld_norm_sell = ore.sell_veldspar(volume=10000, unit="m3", type="N")
    veld_conc_sell = ore.sell_veldspar(volume=10000, unit="m3", type="C")
    veld_dense_sell = ore.sell_veldspar(volume=10000, unit="m3", type="D")
    veld_norm_rep = ore.rep_veldspar(volume=10000, unit="m3", type="N")
    veld_conc_rep = ore.rep_veldspar(volume=10000, unit="m3", type="C")
    veld_dense_rep = ore.rep_veldspar(volume=10000, unit="m3", type="D")
    scord_norm_sell = ore.sell_scordite(volume=10000, unit="m3", type="N")
    scord_cond_sell = ore.sell_scordite(volume=10000, unit="m3", type="C")
    scord_massive_sell = ore.sell_scordite(volume=10000, unit="m3", type="M")
    scord_norm_rep = ore.rep_scordite(volume=10000, unit="m3", type="N")
    scord_cond_rep = ore.rep_scordite(volume=10000, unit="m3", type="C")
    scord_massive_rep = ore.rep_scordite(volume=10000, unit="m3", type="M")



    out_ore_df = pd.DataFrame(data = {'Ore': ["Kernite", "Kernite", "Kernite", "Kernite", "Kernite", "Kernite",
                                          "Pyroxeres", "Pyroxeres", "Pyroxeres", "Pyroxeres", "Pyroxeres", "Pyroxeres",
                                          "Veldspar", "Veldspar", "Veldspar", "Veldspar", "Veldspar", "Veldspar",
                                          "Scordite", "Scordite", "Scordite", "Scordite", "Scordite", "Scordite"],
                                  'Type': ["Normal", "Fiery", "Luminous", "Normal", "Fiery", "Luminous",
                                           "Normal", "Solid", "Viscous", "Normal", "Solid", "Viscous",
                                           "Normal", "Concentrated", "Dense", "Normal", "Concentrated", "Dense",
                                           "Normal", "Condensed", "Massive", "Normal", "Condensed", "Massive"],
                                  'Action': ["Sell", "Sell", "Sell", "Reprocess", "Reprocess", "Reprocess",
                                             "Sell", "Sell", "Sell", "Reprocess", "Reprocess", "Reprocess",
                                             "Sell", "Sell", "Sell", "Reprocess", "Reprocess", "Reprocess",
                                             "Sell", "Sell", "Sell", "Reprocess", "Reprocess", "Reprocess"],
                                  'Price': [kern_norm_sell, kern_fire_sell, kern_lum_sell, kern_norm_rep, kern_fire_rep, kern_lum_rep,
                                            pyro_norm_sell, pyro_solid_sell, pyro_visc_sell, pyro_norm_rep, pyro_solid_rep, pyro_visc_rep,
                                            veld_norm_sell, veld_conc_sell, veld_dense_sell, veld_norm_rep, veld_conc_rep, veld_dense_rep,
                                            scord_norm_sell, scord_cond_sell, scord_massive_sell, scord_norm_rep, scord_cond_rep, scord_massive_rep]}
                          )

    return(out_ore_df)
