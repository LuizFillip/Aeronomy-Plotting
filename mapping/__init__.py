from .plot_regions_over_map import plot_corners, first_of_terminator
from .plot_mag_meridians import plot_mag_meridians, plot_meridian
from .plot_single_tec_map import plot_tec_map
from .plot_ipp_variation_with_terminator import (
    plot_ipp_on_map, 
    plot_roti_timeseries,
    plot_lines
    )
from .plot_roti_and_tec_variation import plot_roti_tec_variation

import base as b 
b.config_labels(fontsize = 25)
