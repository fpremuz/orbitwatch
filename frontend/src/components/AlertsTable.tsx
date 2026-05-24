import type { Alert } from "../types/alert"


interface Props {
  alerts: Alert[]
}


function getSeverityClasses(severity: string) {

  switch (severity) {

    case "CRITICAL":
      return "bg-red-500/20 text-red-400 border border-red-500/30"

    case "WARNING":
      return "bg-yellow-500/20 text-yellow-300 border border-yellow-500/30"

    case "ANOMALY":
      return "bg-purple-500/20 text-purple-300 border border-purple-500/30"

    default:
      return "bg-slate-700 text-slate-300 border border-slate-600"

  }

}


function formatRelativeTime(dateString: string) {

  const now = new Date().getTime()

  const timestamp =
    new Date(dateString).getTime()

  const seconds =
    Math.floor((now - timestamp) / 1000)

  if (seconds < 60) {
    return `${seconds}s ago`
  }

  const minutes =
    Math.floor(seconds / 60)

  if (minutes < 60) {
    return `${minutes}m ago`
  }

  const hours =
    Math.floor(minutes / 60)

  return `${hours}h ago`

}


function AlertsTable({
  alerts,
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

        <div>

          <h2 className="
            text-2xl
            font-semibold
          ">
            Active Alerts
          </h2>

          <p className="
            text-slate-400
            text-sm
            mt-1
          ">
            Real-time telemetry alert feed
          </p>

        </div>


        <div className="
          flex
          items-center
          gap-2
          text-sm
          text-emerald-400
        ">

          <div className="
            w-2
            h-2
            rounded-full
            bg-emerald-400
            animate-pulse
          " />

          LIVE

        </div>

      </div>


      <div className="overflow-x-auto">

        <table className="
          w-full
          text-sm
        ">

          <thead>

            <tr className="
              border-b
              border-slate-800
              text-slate-400
            ">

              <th className="text-left pb-4">
                Severity
              </th>

              <th className="text-left pb-4">
                Parameter
              </th>

              <th className="text-left pb-4">
                Message
              </th>

              <th className="text-left pb-4">
                Time
              </th>

            </tr>

          </thead>


          <tbody>

            {alerts.map((alert) => (

              <tr
                key={alert.id}
                className="
                  border-b
                  border-slate-800/50
                "
              >

                <td className="py-4">

                  <span className={`
                    px-3
                    py-1
                    rounded-full
                    text-xs
                    font-semibold
                    ${getSeverityClasses(alert.severity)}
                  `}>

                    {alert.severity}

                  </span>

                </td>


                <td className="
                  py-4
                  text-cyan-400
                  font-medium
                ">
                  {alert.parameter}
                </td>


                <td className="
                  py-4
                  text-slate-300
                ">
                  {alert.message}
                </td>


                <td className="
                  py-4
                  text-slate-500
                ">
                  {formatRelativeTime(alert.created_at)}
                </td>

              </tr>

            ))}

          </tbody>

        </table>

      </div>

    </div>

  )

}


export default AlertsTable