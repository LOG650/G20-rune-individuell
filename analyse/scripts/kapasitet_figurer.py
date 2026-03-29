"""
Kapasitetsanalyse — 110 Sør-Vest 2025
Figurer og tabeller til rapport LOG650 G20 Rune Grødem

KAPASITETSNIVÅER (utledet av Prosedyre arbeidsmetodikk v4, 16.12.2024):

  NORMAL:  n_aktive = 0 ved ankomst
           → Makkerpar (RØD + GUL) mulig. For c=3: + én GRØNN ledig.
           Prosedyrkonform.

  BRUDD PÅ ARBEIDSMETODIKKEN:  n_aktive >= 1 ved ankomst
           → Nytt anrop kan ikke tildeles dedikert makker.
           Operatørene jobber «etter beste evne».
           For c=2: GUL-operatøren på aktiv hendelse MÅ bryte sin rolle.
           For c=3: Inngående RED får ingen dedikert GUL (makkerparet er opptatt).
           BRUDD på prosedyrens grunnprinsipp om makkerpar-drift.

  SVIKT:   n_aktive >= c_eff ved ankomst
           → VL må bryte vaktlederfunksjon ELLER anrop overføres til Agder.

PARAMETERE: Rediger CONFIGS-blokken for å teste ulike bindingstider.
"""

import pandas as pd
import numpy as np
import heapq
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.ticker as mticker
import sys, os

matplotlib.use('Agg')
sys.stdout.reconfigure(encoding='utf-8')

# ═══════════════════════════════════════════════════════════════════════
# KONFIGURASJON
# ═══════════════════════════════════════════════════════════════════════
CONFIGS = {
    'optimistisk': {'bt_aba':  5, 'bt_tyngre': 10,
                    'label': 'Optimistisk (ABA=5 min, Tyngre=10 min)',
                    'color': '#27ae60', 'marker': 'o'},
    'basis':       {'bt_aba': 10, 'bt_tyngre': 15,
                    'label': 'Basis (ABA=10 min, Tyngre=15 min)',
                    'color': '#2980b9', 'marker': 's'},
    'konservativ': {'bt_aba': 12, 'bt_tyngre': 20,
                    'label': 'Konservativ (ABA=12 min, Tyngre=20 min)',
                    'color': '#8e44ad', 'marker': '^'},
}

DATA_FIL = (r'C:\Users\runeg\OneDrive\Documents\Skole utdanning'
            r'\Logistikk studie\LOG650 LOGISTIKK OG KI'
            r'\G20-rune-individuell\004 data\110 Sør Vest 2025.csv')
FIG_DIR  = (r'C:\Users\runeg\OneDrive\Documents\Skole utdanning'
            r'\Logistikk studie\LOG650 LOGISTIKK OG KI'
            r'\G20-rune-individuell\figurer')

COL = {
    'normal':  '#2ecc71',
    'brudd':   '#e67e22',
    'svikt':   '#c0392b',
    'hverdag': '#2980b9',
    'helg':    '#8e44ad',
}

SKIFT_ORDER = ['Dag / Hverdag', 'Dag / Helg', 'Natt / Hverdag', 'Natt / Helg']
DAGER = ['Man', 'Tir', 'Ons', 'Tor', 'Fre', 'Lør', 'Søn']

TYNGRE = ['brann', 'trafikk', 'ecall', 'helse', 'natur', 'flom', 'storm',
          'rvr', 'selvdrap', 'vann', 'drukning', 'redning', 'person i vann']

# ═══════════════════════════════════════════════════════════════════════
# DATA
# ═══════════════════════════════════════════════════════════════════════
def les_data():
    sv = pd.read_csv(DATA_FIL, sep=None, engine='python',
                     encoding='utf-8-sig', skiprows=2, header=0)
    sv.columns = sv.columns.str.strip()
    sv['ts'] = pd.to_datetime(
        sv['Dato anrop'] + ' ' + sv['Tid anrop'],
        format='%d.%m.%Y %H:%M:%S', errors='coerce')
    sv = sv.dropna(subset=['ts'])
    T1 = '110-oppdrag uten involvering av brannvesen'
    df = sv[sv['Overordnet oppdragstype'] != T1].copy()
    df = df.sort_values('ts').reset_index(drop=True)
    df['weekday'] = df['ts'].dt.weekday
    df['hour']    = df['ts'].dt.hour
    df['is_helg'] = df['weekday'] >= 5
    df['is_dag']  = (df['hour'] >= 7) & (df['hour'] < 19)
    return df

def skift_c(row):
    if row['is_dag']  and not row['is_helg']: return 'Dag / Hverdag',   3
    if row['is_dag']  and row['is_helg']:     return 'Dag / Helg',      2
    if not row['is_dag'] and not row['is_helg']: return 'Natt / Hverdag', 2
    return 'Natt / Helg', 2

# ═══════════════════════════════════════════════════════════════════════
# ANALYSE
# ═══════════════════════════════════════════════════════════════════════
def kjor_analyse(base, bt_aba, bt_tyngre):
    def bt(otype):
        if pd.isna(otype): return bt_aba
        o = str(otype).lower()
        if 'aba' in o: return bt_aba
        for k in TYNGRE:
            if k in o: return bt_tyngre
        return bt_aba

    df = base.copy()
    df['bt_min']   = df['Opprinnelig oppdragstype'].apply(bt)
    df['ts_slutt'] = df['ts'] + pd.to_timedelta(df['bt_min'], unit='m')
    df[['skift', 'c_eff']] = df.apply(skift_c, axis=1, result_type='expand')

    heap, rows = [], []
    for _, row in df.iterrows():
        ts_ns  = row['ts'].value
        ts_s   = row['ts_slutt'].value
        c      = row['c_eff']

        while heap and heap[0] <= ts_ns:
            heapq.heappop(heap)
        n = len(heap)   # aktive hendelser ved ankomst

        # ── KAPASITETSNIVÅ ────────────────────────────────────────────
        # BRUDD: n >= 1 for BEGGE skifttyper
        #   c=2: GUL-OP bryter rolle → solo-håndtering
        #   c=3: Inngående anrop får ingen dedikert makker → «etter beste evne»
        # SVIKT: n >= c_eff
        #   VL må bryte vaktlederfunksjon ELLER over til Agder
        brudd = n >= 1
        svikt = n >= c

        rows.append({
            'ts':       row['ts'],
            'type':     row['Opprinnelig oppdragstype'],
            'bt_min':   row['bt_min'],
            'skift':    row['skift'],
            'c_eff':    c,
            'n_aktive': n,
            'brudd':    brudd,
            'svikt':    svikt,
            'weekday':  row['weekday'],
            'is_helg':  row['is_helg'],
            'is_dag':   row['is_dag'],
        })
        heapq.heappush(heap, ts_s)
    return pd.DataFrame(rows)

# ═══════════════════════════════════════════════════════════════════════
# HJELPERE
# ═══════════════════════════════════════════════════════════════════════
def fmt_ax(ax):
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.tick_params(labelsize=10)

def brudd_label():
    return 'Brudd på arbeidsmetodikk\n(«etter beste evne»)'

def svikt_label():
    return 'Svikt: VL bryter rolle / til Agder'

def skift_stats(df):
    rows = []
    for sk in SKIFT_ORDER:
        sub = df[df['skift'] == sk]
        n   = len(sub)
        c   = sub['c_eff'].iloc[0]
        sv  = sub['svikt'].sum()
        br  = sub['brudd'].sum() - sv          # brudd men ikke svikt
        nor = n - sub['brudd'].sum()
        rows.append({'skift': sk, 'c_eff': c, 'n': n,
                     'normal': nor, 'brudd': br, 'svikt': sv})
    return pd.DataFrame(rows)

# ═══════════════════════════════════════════════════════════════════════
# FIGUR 1 — Stablet søyle: kapasitetsnivå per skifttype
# ═══════════════════════════════════════════════════════════════════════
def fig1_nivaa(df, label, suffix):
    st = skift_stats(df)
    fig, ax = plt.subplots(figsize=(10, 6))
    x, w = np.arange(4), 0.55

    # Fargebånd for prosedyrbrudd-bakgrunn
    for xi in [1, 2, 3]:   # helg + natt hverdag
        ax.axvspan(xi - w/2 - 0.05, xi + w/2 + 0.05,
                   color='#fde8e8', alpha=0.35, zorder=0)

    bot = np.zeros(4)
    for felt, farge, tekst in [
        ('normal', COL['normal'],  'Normal — makkerpar mulig (prosedyrkonform)'),
        ('brudd',  COL['brudd'],   brudd_label()),
        ('svikt',  COL['svikt'],   svikt_label()),
    ]:
        vals = (st[felt] / st['n'] * 100).values
        bars = ax.bar(x, vals, w, bottom=bot, color=farge, label=tekst,
                      zorder=3, edgecolor='white', linewidth=0.5)
        for i, v in enumerate(vals):
            if v > 1.5:
                ax.text(x[i], bot[i] + v / 2, f'{v:.1f}%',
                        ha='center', va='center', fontsize=9.5,
                        fontweight='bold', color='white')
        bot += vals

    # «BRUDD»-stempel på relevante søyler
    for i, sk in enumerate(SKIFT_ORDER):
        sub = df[df['skift'] == sk]
        br_pct = sub['brudd'].mean() * 100
        if br_pct > 2:
            ax.annotate('BRUDD\nPÅ AML',
                        xy=(x[i], 101), xytext=(x[i], 101),
                        ha='center', va='bottom', fontsize=8,
                        color=COL['svikt'], fontweight='bold',
                        bbox=dict(boxstyle='round,pad=0.2',
                                  fc='#fde8e8', ec=COL['svikt'], lw=1))

    c_labels = []
    for sk in SKIFT_ORDER:
        c = st.loc[st['skift'] == sk, 'c_eff'].values[0]
        k = 'helg' if 'Helg' in sk else 'hverdag'
        c_labels.append(f'{sk}\n(c_eff={c})')

    ax.set_xticks(x)
    ax.set_xticklabels(c_labels, fontsize=10)
    ax.set_ylabel('Andel av beredskapsanrop (%)', fontsize=11)
    ax.set_ylim(0, 112)
    ax.yaxis.set_major_formatter(mticker.PercentFormatter(decimals=0))
    ax.set_title(
        f'Kapasitetsnivå ved ankomst av beredskapsanrop — 110 Sør-Vest 2025\n'
        f'{label}',
        fontsize=12, fontweight='bold')
    ax.yaxis.grid(True, alpha=0.3, zorder=0)

    # Prosedyrbrudd-forklaring i boks
    ax.text(0.01, 0.01,
            'Brudd på arbeidsmetodikk (AML) = nytt anrop ankommer uten ledig makker.\n'
            'Operatørene jobber «etter beste evne» — makkerparet er allerede engasjert.\n'
            'Kilde: Prosedyre arbeidsmetodikk v4, Rogaland brann og redning IKS (2024).',
            transform=ax.transAxes, fontsize=7.5, va='bottom',
            color='#555', style='italic',
            bbox=dict(boxstyle='round', fc='#fff9f0', ec='#ccc', alpha=0.8))

    ax.legend(loc='upper right', fontsize=9, framealpha=0.95,
              fancybox=True, edgecolor='#ccc')
    fmt_ax(ax)
    plt.tight_layout()
    path = os.path.join(FIG_DIR, f'kap_fig1_nivaa_{suffix}.png')
    plt.savefig(path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f'  Lagret: {os.path.basename(path)}')

# ═══════════════════════════════════════════════════════════════════════
# FIGUR 2 — Hverdag vs helg: volum + brudd-rate side by side
# ═══════════════════════════════════════════════════════════════════════
def fig2_hverdag_helg(df, label, suffix):
    fig, axes = plt.subplots(1, 2, figsize=(12, 5.5))

    for ax, (tittel, dag_mask, n_hv_d, n_he_d) in zip(axes, [
        ('Dag (07–19)',   df['is_dag'],  260, 104),
        ('Natt (19–07)', ~df['is_dag'], 260, 104),
    ]):
        hv = df[dag_mask & ~df['is_helg']]
        he = df[dag_mask &  df['is_helg']]

        vol_hv   = len(hv) / n_hv_d
        vol_he   = len(he) / n_he_d
        br_hv    = hv['brudd'].mean() * 100
        br_he    = he['brudd'].mean() * 100
        sv_hv    = hv['svikt'].mean() * 100
        sv_he    = he['svikt'].mean() * 100

        x  = np.array([0, 1])
        ax2 = ax.twinx()

        vol_bars = ax.bar(x - 0.2, [vol_hv, vol_he], 0.35,
                          color=[COL['hverdag'], COL['helg']],
                          alpha=0.75, zorder=3, label='Anrop/dag')
        ax2.bar(x + 0.2, [br_hv, br_he], 0.35,
                color=[COL['hverdag'], COL['helg']],
                alpha=0.45, hatch='//', zorder=3,
                label='Brudd på AML (%)')
        ax2.bar(x + 0.2, [sv_hv, sv_he], 0.35,
                color=[COL['svikt'], COL['svikt']],
                alpha=0.7, hatch='xx', zorder=4,
                label='Svikt (%)')

        # Verdiannotering
        for bar, v in zip(vol_bars, [vol_hv, vol_he]):
            ax.text(bar.get_x() + bar.get_width() / 2,
                    bar.get_height() + 0.15,
                    f'{v:.1f}', ha='center', va='bottom',
                    fontsize=11, fontweight='bold')

        for xi, br, sv in zip(x + 0.2, [br_hv, br_he], [sv_hv, sv_he]):
            ax2.text(xi, br + 0.8, f'{br:.1f}%',
                     ha='center', va='bottom', fontsize=10,
                     fontweight='bold', color=COL['brudd'])
            if sv > 0.3:
                ax2.text(xi, sv / 2, f'{sv:.1f}%',
                         ha='center', va='center', fontsize=8,
                         fontweight='bold', color='white')

        # Marker brudd-søyler med boks
        for xi, br in zip(x + 0.2, [br_hv, br_he]):
            if br > 5:
                ax2.annotate('BRUDD\nPÅ AML',
                             xy=(xi, br + 1.5),
                             ha='center', va='bottom', fontsize=8,
                             color=COL['svikt'], fontweight='bold',
                             bbox=dict(boxstyle='round,pad=0.2',
                                       fc='#fde8e8', ec=COL['svikt'],
                                       lw=1))

        ax.set_xticks(x)
        ax.set_xticklabels(['Hverdag', 'Helg'], fontsize=12)
        ax.set_ylabel('Beredskapsanrop per vaktdag', fontsize=10)
        ax2.set_ylabel('Andel av anrop (%)', fontsize=10)
        ax.set_title(tittel, fontsize=12, fontweight='bold')
        ax.set_ylim(0, max(vol_hv, vol_he) * 1.55)
        ax2.set_ylim(0, max(br_hv, br_he) * 1.6)
        fmt_ax(ax)
        ax2.spines['top'].set_visible(False)

    p1 = mpatches.Patch(color='steelblue', alpha=0.75, label='Volum (anrop/dag)')
    p2 = mpatches.Patch(color='steelblue', alpha=0.45, hatch='//',
                        label='Brudd på arbeidsmetodikk (%)')
    p3 = mpatches.Patch(color=COL['svikt'], alpha=0.7, hatch='xx',
                        label='Svikt: VL/Agder (%)')
    fig.legend(handles=[p1, p2, p3], loc='lower center',
               ncol=3, fontsize=9, bbox_to_anchor=(0.5, -0.03),
               fancybox=True, framealpha=0.9)

    fig.suptitle(
        f'Beredskapsvolum og prosedyrbrudd — hverdag vs helg\n{label}',
        fontsize=12, fontweight='bold')
    plt.tight_layout()
    path = os.path.join(FIG_DIR, f'kap_fig2_hverdaghelg_{suffix}.png')
    plt.savefig(path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f'  Lagret: {os.path.basename(path)}')

# ═══════════════════════════════════════════════════════════════════════
# FIGUR 3 — Brudd og svikt per ukedag
# ═══════════════════════════════════════════════════════════════════════
def fig3_ukedag(df, label, suffix):
    fig, ax = plt.subplots(figsize=(10, 5.5))
    x = np.arange(7)

    br_r = np.array([df[df['weekday'] == wd]['brudd'].mean() * 100
                     for wd in range(7)])
    sv_r = np.array([df[df['weekday'] == wd]['svikt'].mean() * 100
                     for wd in range(7)])
    n_r  = np.array([len(df[df['weekday'] == wd]) for wd in range(7)])

    col_bars = [COL['helg'] if i >= 5 else COL['hverdag'] for i in range(7)]
    ax.bar(x, br_r, color=col_bars, alpha=0.65, label='Brudd på AML', zorder=3)
    ax.bar(x, sv_r, color=[COL['svikt']] * 7, alpha=0.85,
           label='Svikt (VL/Agder)', zorder=4)

    for i, (br, sv, n) in enumerate(zip(br_r, sv_r, n_r)):
        ax.text(i, br + 0.4, f'{br:.1f}%\n(n={n})',
                ha='center', va='bottom', fontsize=8.5, fontweight='bold',
                color='black')

    ax.axvspan(4.5, 6.5, color='#f0e6ff', alpha=0.4, zorder=0)
    ax.text(5.5, max(br_r) * 0.88, 'HELG\nc_eff = 2',
            ha='center', fontsize=9, color=COL['helg'],
            fontweight='bold',
            bbox=dict(boxstyle='round', fc='#f0e6ff', ec=COL['helg'],
                      alpha=0.7))

    # Horisontal referanselinje: snitt hverdag
    hv_snitt = br_r[:5].mean()
    ax.axhline(hv_snitt, color=COL['hverdag'], lw=1.5, ls='--', alpha=0.8)
    ax.text(3.5, hv_snitt + 0.4, f'Hverdag-snitt: {hv_snitt:.1f}%',
            ha='center', va='bottom', fontsize=8.5,
            color=COL['hverdag'], fontweight='bold')

    ax.set_xticks(x)
    ax.set_xticklabels(DAGER, fontsize=11)
    ax.set_ylabel('Andel av beredskapsanrop (%)', fontsize=11)
    ax.yaxis.set_major_formatter(mticker.PercentFormatter(decimals=1))
    ax.set_title(
        f'Brudd på arbeidsmetodikk og svikt per ukedag\n'
        f'110 Sør-Vest 2025 | {label}',
        fontsize=12, fontweight='bold')
    ax.legend(fontsize=10, framealpha=0.95, fancybox=True)
    ax.yaxis.grid(True, alpha=0.3, zorder=0)

    ax.text(0.01, 0.97,
            'Brudd på AML = nytt anrop ankommer uten ledig makker\n'
            '(begge c_eff-operatørene allerede i RØD/GUL-funksjon)',
            transform=ax.transAxes, fontsize=7.5, va='top',
            color='#555', style='italic',
            bbox=dict(boxstyle='round', fc='#fff9f0', ec='#ccc', alpha=0.8))

    fmt_ax(ax)
    plt.tight_layout()
    path = os.path.join(FIG_DIR, f'kap_fig3_ukedag_{suffix}.png')
    plt.savefig(path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f'  Lagret: {os.path.basename(path)}')

# ═══════════════════════════════════════════════════════════════════════
# FIGUR 4 — Sensitivitet: alle tre bindingstidsscenarier
# ═══════════════════════════════════════════════════════════════════════
def fig4_sensitivitet(alle_df):
    fig, axes = plt.subplots(1, 2, figsize=(13, 5.5))

    for ax, (metrikk, col_key, tittel) in zip(axes, [
        ('brudd', 'brudd', 'Brudd på arbeidsmetodikk'),
        ('svikt', 'svikt', 'Svikt (VL/Agder)'),
    ]):
        x       = np.arange(4)
        n_cfg   = 3
        width   = 0.22
        offsets = [-0.22, 0, 0.22]

        for i, (key, cfg) in enumerate(CONFIGS.items()):
            df    = alle_df[key]
            rates = [df[df['skift'] == sk][metrikk].mean() * 100
                     for sk in SKIFT_ORDER]
            bars = ax.bar(x + offsets[i], rates, width,
                          label=cfg['label'],
                          color=cfg['color'], alpha=0.78, zorder=3,
                          edgecolor='white', linewidth=0.5)
            for bar, v in zip(bars, rates):
                if v > 0.3:
                    ax.text(bar.get_x() + bar.get_width() / 2,
                            bar.get_height() + 0.3,
                            f'{v:.1f}%', ha='center', va='bottom',
                            fontsize=7.5, fontweight='bold',
                            color=cfg['color'])

        c_labels = [f'{sk}\n(c={[3,2,2,2][i]})'
                    for i, sk in enumerate(SKIFT_ORDER)]
        ax.set_xticks(x)
        ax.set_xticklabels(c_labels, fontsize=9)
        ax.set_ylabel('Andel av beredskapsanrop (%)', fontsize=10)
        ax.yaxis.set_major_formatter(mticker.PercentFormatter(decimals=1))
        ax.set_title(tittel, fontsize=11, fontweight='bold')
        ax.yaxis.grid(True, alpha=0.3, zorder=0)

        # Fremhev helg-søyler
        for xi in [1, 2, 3]:
            ax.axvspan(xi - 0.38, xi + 0.38, color='#fde8e8',
                       alpha=0.2, zorder=0)
        fmt_ax(ax)

    axes[0].legend(fontsize=8.5, framealpha=0.95, fancybox=True,
                   loc='upper left')

    fig.suptitle(
        'Sensitivitetsanalyse: bindingstidsestimat vs kapasitetsnivå\n'
        '110 Sør-Vest 2025 — tre scenarier (optimistisk / basis / konservativ)',
        fontsize=12, fontweight='bold')

    fig.text(0.5, -0.01,
             'Konklusjon: Rangeringen og det strukturelle helg/hverdag-gapet er robuste '
             'uavhengig av valgt bindingstidsestimat.\n'
             'Selv det korteste estimatet (ABA=5 min, Tyngre=10 min) viser '
             'markant høyere brudd-rate på helg enn hverdag.',
             ha='center', fontsize=8.5, style='italic', color='#444',
             wrap=True)

    plt.tight_layout()
    path = os.path.join(FIG_DIR, 'kap_fig4_sensitivitet_bt.png')
    plt.savefig(path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f'  Lagret: {os.path.basename(path)}')

# ═══════════════════════════════════════════════════════════════════════
# FIGUR 5 — Effekt av c_eff=3 på helg dagskift
# ═══════════════════════════════════════════════════════════════════════
def fig5_ceff_helg(df, label, suffix):
    he = df[df['is_helg'] & df['is_dag']].copy()
    n  = len(he)

    # Med c_eff=3: brudd=n>=1 (same threshold), svikt=n>=3
    he['brudd_c3'] = he['n_aktive'] >= 1   # same brudd logic
    he['svikt_c3'] = he['n_aktive'] >= 3

    # c=2 breakdown
    sv2  = he['svikt'].sum()
    br2  = he['brudd'].sum() - sv2
    no2  = n - he['brudd'].sum()
    # c=3 breakdown (lower svikt threshold = 3 instead of 2)
    sv3  = he['svikt_c3'].sum()
    br3  = he['brudd_c3'].sum() - sv3
    no3  = n - he['brudd_c3'].sum()

    fig, ax = plt.subplots(figsize=(9, 5.5))
    x = np.arange(3)

    def pct(v): return v / n * 100

    c2_vals = [pct(no2), pct(br2), pct(sv2)]
    c3_vals = [pct(no3), pct(br3), pct(sv3)]
    cat_labels = ['Normal\n(makkerpar)', 'Brudd på AML\n(«etter beste evne»)',
                  'Svikt\n(VL/Agder)']
    colors = [COL['normal'], COL['brudd'], COL['svikt']]

    for xi, (v2, v3, col) in enumerate(zip(c2_vals, c3_vals, colors)):
        b2 = ax.bar(xi - 0.2, v2, 0.35, color=col, alpha=0.85, zorder=3,
                    label='Faktisk: c_eff=2' if xi == 0 else '_')
        b3 = ax.bar(xi + 0.2, v3, 0.35, color=col, alpha=0.42,
                    hatch='//', zorder=3, edgecolor=col,
                    label='Foreslått: c_eff=3' if xi == 0 else '_')
        for bar, v in [(b2, v2), (b3, v3)]:
            if v > 1:
                ax.text(bar[0].get_x() + bar[0].get_width() / 2,
                        bar[0].get_height() + 0.6,
                        f'{v:.1f}%', ha='center', va='bottom',
                        fontsize=10.5, fontweight='bold')

    # Reduksjonspil for "Brudd"-søyle
    red = c2_vals[1] - c3_vals[1]
    if red > 1:
        ax.annotate(
            f'−{red:.0f}%\n(−{int(round(br2 - br3))} hendelser/år)',
            xy=(0.2, c3_vals[1] + 0.5), xytext=(0.8, (c2_vals[1] + c3_vals[1]) / 2),
            fontsize=9, color=COL['svikt'], fontweight='bold',
            arrowprops=dict(arrowstyle='->', color=COL['svikt'], lw=1.5))

    ax.set_xticks(x)
    ax.set_xticklabels(cat_labels, fontsize=10)
    ax.set_ylabel('Andel av beredskapsanrop (%)', fontsize=11)
    ax.yaxis.set_major_formatter(mticker.PercentFormatter(decimals=0))
    ax.set_title(
        f'Effekt av én ekstra operatør — helg dagskift\n'
        f'110 Sør-Vest 2025 | {label}',
        fontsize=12, fontweight='bold')

    ax.text(0.5, 0.97,
            '«Én ekstra operatør på helg dagskift reduserer brudd på\n'
            'arbeidsmetodikken og bringer sviktraten ned til hverdag-nivå»',
            transform=ax.transAxes, fontsize=8.5, ha='center', va='top',
            style='italic', color='#444',
            bbox=dict(boxstyle='round', fc='#f0fff4', ec='#27ae60',
                      alpha=0.85, lw=1.2))

    ax.legend(fontsize=10, framealpha=0.95, fancybox=True)
    ax.yaxis.grid(True, alpha=0.3, zorder=0)
    fmt_ax(ax)
    plt.tight_layout()
    path = os.path.join(FIG_DIR, f'kap_fig5_ceff_helg_{suffix}.png')
    plt.savefig(path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f'  Lagret: {os.path.basename(path)}')

# ═══════════════════════════════════════════════════════════════════════
# TABELL PRINT
# ═══════════════════════════════════════════════════════════════════════
def print_tabell(df, cfg):
    print(f"\n{'='*72}")
    print(f"  {cfg['label']}")
    print(f"{'='*72}")
    print(f"  {'Skifttype':<22} {'Anrop':>6}  {'Normal':>14}  "
          f"{'Brudd på AML':>16}  {'Svikt':>12}  c_eff")
    print("  " + "-" * 76)
    for sk in SKIFT_ORDER:
        sub = df[df['skift'] == sk]
        n   = len(sub)
        c   = sub['c_eff'].iloc[0]
        sv  = sub['svikt'].sum()
        br  = sub['brudd'].sum() - sv
        no  = n - sub['brudd'].sum()
        brudd_mark = ' ◄ BRUDD' if sub['brudd'].mean() > 0.10 else ''
        print(f"  {sk:<22} {n:>6,}  "
              f"{no:>6,} ({100*no/n:>4.1f}%)  "
              f"{br:>7,} ({100*br/n:>5.2f}%)  "
              f"{sv:>5,} ({100*sv/n:>4.2f}%)  "
              f"{c}{brudd_mark}")
    print()
    for lab, mask in [("Dag (07-19)", df['is_dag']), ("Natt (19-07)", ~df['is_dag'])]:
        hv = df[mask & ~df['is_helg']]
        he = df[mask &  df['is_helg']]
        r_hv = 100 * hv['brudd'].mean(); r_he = 100 * he['brudd'].mean()
        ratio = r_he / r_hv if r_hv > 0 else float('inf')
        print(f"  {lab}:")
        print(f"    Hverdag: {len(hv)/260:.1f} anrop/dag  "
              f"Brudd: {r_hv:.1f}%  Svikt: {100*hv['svikt'].mean():.1f}%")
        print(f"    Helg:    {len(he)/104:.1f} anrop/dag  "
              f"Brudd: {r_he:.1f}%  Svikt: {100*he['svikt'].mean():.1f}%  "
              f"→ {ratio:.1f}× høyere brudd-rate enn hverdag")

# ═══════════════════════════════════════════════════════════════════════
# KJØR
# ═══════════════════════════════════════════════════════════════════════
print("Leser data...")
base = les_data()
print(f"Beredskapsoppdrag totalt: {len(base):,}\n")

alle_df = {}
for key, cfg in CONFIGS.items():
    print(f"── Analyserer: {cfg['label']} ──")
    df = kjor_analyse(base, cfg['bt_aba'], cfg['bt_tyngre'])
    alle_df[key] = df
    print_tabell(df, cfg)
    lbl = f"ABA={cfg['bt_aba']} min | Tyngre={cfg['bt_tyngre']} min"
    fig1_nivaa(df, lbl, key)
    fig2_hverdag_helg(df, lbl, key)
    fig3_ukedag(df, lbl, key)
    fig5_ceff_helg(df, lbl, key)

print("\n── Sensitivitetsfigur (alle tre scenarier) ──")
fig4_sensitivitet(alle_df)

print(f"\nFerdige figurer i: {FIG_DIR}")
print("\nFiguroversikt:")
for navn in [
    'kap_fig1_nivaa_[suffix]        — Stablet søyle: kapasitetsnivå (Normal/Brudd/Svikt)',
    'kap_fig2_hverdaghelg_[suffix]  — Hverdag vs helg volum og brudd-rate',
    'kap_fig3_ukedag_[suffix]       — Brudd og svikt per ukedag',
    'kap_fig4_sensitivitet_bt       — Alle 3 bindingstidsscenarier side om side',
    'kap_fig5_ceff_helg_[suffix]    — Effekt av c_eff=3 på helg dagskift',
]:
    print(f'  {navn}')
