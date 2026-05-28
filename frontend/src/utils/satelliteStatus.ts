export function getSatelliteStatus(
  healthScore: number
) {

  if (healthScore >= 90) {
    return "HEALTHY"
  }

  if (healthScore >= 70) {
    return "WARNING"
  }

  return "CRITICAL"
}