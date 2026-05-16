interface Props {
  connected: boolean;
}

export default function ConnectionStatus({
  connected,
}: Props) {
  return (
    <div
      className={`px-3 py-2 rounded text-white font-semibold w-fit ${
        connected
          ? "bg-green-600"
          : "bg-red-600"
      }`}
    >
      {connected
        ? "Connected"
        : "Disconnected"}
    </div>
  );
}