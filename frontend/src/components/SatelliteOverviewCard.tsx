import type { SatelliteOverview } from "../types/satelliteOverview"

import SatelliteStatusBadge from "./SatelliteStatusBadge"


interface Props {

  satellite: SatelliteOverview

}


function SatelliteOverviewCard({
  satellite,
}: Props) {

  return (

    <div className="
      bg-slate-900
      border
      border-slate-800
      rounded-2xl
      p-6
    ">

      <div className="
        flex
        items-center
        justify-between
        mb-6
      ">

        <h2 className="
          text-2xl
          font-semibold
        ">
          {satellite.name}
        </h2>

        <SatelliteStatusBadge
          level={
            satellite.latest_alert_level
          }
        />

      </div>


      <div className="
        space-y-4
        text-sm
      ">

        <div className="
          flex
          justify-between
        ">

          <span className="text-slate-400">
            NORAD ID
          </span>

          <span className="text-cyan-400">
            {satellite.norad_id}
          </span>

        </div>


        <div className="
          flex
          justify-between
        ">

          <span className="text-slate-400">
            Active Alerts
          </span>

          <span className="
            text-white
            font-semibold
          ">
            {satellite.alert_count}
          </span>

        </div>


        <div className="
          flex
          justify-between
        ">

          <span className="text-slate-400">
            Latest Alert
          </span>

          <span className="
            text-yellow-400
            font-semibold
          ">

            {satellite.latest_alert_level
              ?? "NOMINAL"}

          </span>

        </div>

      </div>

    </div>

  )

}


export default SatelliteOverviewCard