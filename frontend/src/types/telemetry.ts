export interface TelemetryPoint {

  timestamp: string

  timestampMs: number

  value: number

}


export interface TelemetryParameter {

  name: string

  value: number

}


export interface TelemetryEvent {

  event_id: string

  satellite_id: string

  timestamp: string

  parameters: TelemetryParameter[]

}