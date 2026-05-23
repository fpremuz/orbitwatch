import type {
  SatelliteOverview,
} from "../types/satelliteOverview"

interface Props {

  satellite: SatelliteOverview

}

function SatelliteOverviewCard({
  satellite,
}: Props) {

  function getStatusColor() {

    switch (satellite.status) {

      case "ONLINE":
        return "bg-green-500"

      case "DELAYED":
        return "bg-yellow-500"

      case "OFFLINE":
        return "bg-red-500"

      default:
        return "bg-slate-500"

    }

  }

  return (

    <div className="
      bg-slate-900
      rounded-xl
      p-6
      border
      border-slate-800
    ">

      <div className="
        flex
        items-center
        justify-between
        mb-4
      ">

        <h2 className="
          text-xl
          font-semibold
        ">
          {satellite.name}
        </h2>

        <div className="
          flex
          items-center
          gap-2
        ">

          <div className={`
            w-3
            h-3
            rounded-full
            ${getStatusColor()}
          `} />

          <span className="text-sm">
            {satellite.status}
          </span>

        </div>

      </div>

      <div className="
        text-sm
        text-slate-400
        space-y-2
      ">

        <p>
          NORAD ID: {satellite.norad_id}
        </p>

        <p>
          Orbit Type: {satellite.orbit_type}
        </p>

        <p>
          Last Seen:
          {" "}
          {satellite.last_seen
            ? new Date(
                satellite.last_seen
              ).toLocaleTimeString()
            : "Never"}
        </p>

      </div>

    </div>

  )

}

export default SatelliteOverviewCard