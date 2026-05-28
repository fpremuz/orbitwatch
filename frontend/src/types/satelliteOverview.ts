export interface SatelliteOverview {

  id: string

  name: string

  norad_id: number

  orbit_type: string

  last_seen: string | null

  health_score: number

  status:
    | "ONLINE"
    | "DELAYED"
    | "OFFLINE"

}