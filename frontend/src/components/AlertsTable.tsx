import type { Alert } from "../types/alert"

import AlertLevelBadge from "./AlertLevelBadge"

interface Props {
  alerts: Alert[]
}

function AlertsTable({ alerts }: Props) {

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6">

      <div className="flex items-center justify-between mb-6">

        <h2 className="text-2xl font-semibold">
          Active Alerts
        </h2>

        <div className="text-sm text-slate-400">
          {alerts.length} alerts
        </div>

      </div>

      <div className="overflow-x-auto">

        <table className="w-full text-sm">

          <thead>

            <tr className="text-left text-slate-400 border-b border-slate-800">

              <th className="pb-3">
                Severity
              </th>

              <th className="pb-3">
                Parameter
              </th>

              <th className="pb-3">
                Message
              </th>

              <th className="pb-3">
                Timestamp
              </th>

            </tr>

          </thead>

          <tbody>

            {alerts.map((alert) => (

              <tr
                key={alert.id}
                className="border-b border-slate-800 hover:bg-slate-800/40 transition-all"
              >

                <td className="py-4">
                  <AlertLevelBadge
                    level={alert.level}
                  />
                </td>

                <td className="py-4 text-cyan-400">
                  {alert.parameter}
                </td>

                <td className="py-4 text-slate-300">
                  {alert.message}
                </td>

                <td className="py-4 text-slate-500">
                  {
                    new Date(
                      alert.created_at
                    ).toLocaleString()
                  }
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