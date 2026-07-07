"""Hydrogen bonds: protein-protein and protein-solvent (streamed, shell-restricted)."""

from __future__ import annotations

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from MDAnalysis.analysis.hydrogenbonds import HydrogenBondAnalysis as HBA

from mdforge.core.base import BaseAnalysis
from mdforge import plotting
from mdforge import statistics as st
from mdforge.plotting import PALETTE

WATER = "resname TIP3 SOL WAT HOH SPC TIP4"


class HydrogenBonds(BaseAnalysis):
    name = "hbonds"
    label = "Hydrogen bonds"
    category = "interactions"
    required_files = {"trajectory", "topology"}
    supported_systems = {"*"}
    default_params = {"stride": 20, "shell": 4.5, "window": 10}
    outputs = ["results/hbonds_timeseries.csv", "figures/hbonds_timeseries.png"]

    def run(self, ctx) -> dict:
        p = self.params(ctx)
        plotting.set_style()
        u = ctx.full_universe()
        stride = p["stride"]

        hba_pp = HBA(universe=u)
        hba_pp.hydrogens_sel = hba_pp.guess_hydrogens("protein")
        hba_pp.acceptors_sel = hba_pp.guess_acceptors("protein")
        hba_pp.run(step=stride)
        counts_pp = hba_pp.count_by_time()
        n = len(counts_pp)
        dt = u.trajectory.dt
        times = (u.trajectory[0].time + np.arange(n) * stride * dt) / 1000.0

        counts_ps = np.zeros(n)
        if ctx.system.flags.get("has_water"):
            shell = p["shell"]
            wo = f"({WATER}) and name OH2 OW OW1 O"
            wh = f"({WATER}) and name H1 H2 HW1 HW2"
            pw = HBA(universe=u, update_selections=True)
            pw.hydrogens_sel = pw.guess_hydrogens("protein")
            pw.acceptors_sel = f"({wo}) and around {shell} protein"
            pw.run(step=stride)
            wp = HBA(universe=u, update_selections=True)
            wp.hydrogens_sel = f"({wh}) and around {shell} protein"
            wp.acceptors_sel = wp.guess_acceptors("protein")
            wp.run(step=stride)
            counts_ps = (pw.count_by_time() + wp.count_by_time())[:n]

        ctx.write_csv(pd.DataFrame({"time_ns": times,
                                    "hbonds_protein_protein": counts_pp,
                                    "hbonds_protein_solvent": counts_ps}),
                      "hbonds_timeseries.csv")

        fig, (a1, a2) = plt.subplots(2, 1, figsize=(7.6, 6.4), sharex=True)
        a1.plot(times, counts_pp, color=PALETTE["primary"], alpha=0.4, lw=1.0)
        a1.plot(times, st.moving_average(counts_pp, p["window"]),
                color=PALETTE["primary"], lw=2.2)
        a1.set_ylabel("Protein-protein\nH-bonds"); a1.set_title("Hydrogen bonds over time")
        a2.plot(times, counts_ps, color=PALETTE["secondary"], alpha=0.4, lw=1.0)
        a2.plot(times, st.moving_average(counts_ps, p["window"]),
                color=PALETTE["secondary"], lw=2.2)
        a2.set_ylabel("Protein-solvent\nH-bonds"); a2.set_xlabel("Time (ns)")
        for a in (a1, a2):
            a.spines["top"].set_visible(False); a.spines["right"].set_visible(False)
        plotting.save_figure(fig, ctx.fig_path("hbonds_timeseries"), dpi=ctx.config.dpi)

        return {"protein_protein": st.describe(counts_pp, "hbonds_pp"),
                "protein_solvent": st.describe(counts_ps, "hbonds_ps"),
                "figure": "hbonds_timeseries"}
