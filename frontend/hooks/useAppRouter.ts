import { useRouter } from "next/navigation";

export function useAppRouter() {
  const router = useRouter();

  return {
    toHome: () => router.push("/"),
    toRange: () => router.push("/range"),
    toSettings: () => router.push("/settings"),
    toResult: () => router.push("/result"),
    back: () => router.back(),
  };
}