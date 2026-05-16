import type { TelemetryEvent } from "../../hooks/useTelemetrySocket";

interface Props {
  events: TelemetryEvent[];
}

export default function TelemetryFeed({
  events,
}: Props) {
  return (
    <div className="space-y-4">
      {events.map((event, index) => (
        <div
          key={index}
          className="border rounded p-4 shadow"
        >
          <div className="font-bold">
            Satellite:
          </div>

          <div className="mb-2">
            {event.satellite_id}
          </div>

          <div className="font-bold">
            Timestamp:
          </div>

          <div className="mb-2">
            {event.timestamp}
          </div>

          <div className="font-bold mb-1">
            Parameters
          </div>

          <ul className="list-disc pl-5">
            {event.parameters.map(
              (parameter, idx) => (
                <li key={idx}>
                  {parameter.name}:{" "}
                  {parameter.value}
                </li>
              )
            )}
          </ul>
        </div>
      ))}
    </div>
  );
}