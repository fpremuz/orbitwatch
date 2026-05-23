export interface SatelliteOverview {

  id: string

  name: string

  norad_id: number

  orbit_type: string

  last_seen: string | null

  status:
    | "ONLINE"
    | "DELAYED"
    | "OFFLINE"

}