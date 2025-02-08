import { cn } from "@/lib/utils"

// Components for Skeleton screen
// Function: placeholder animation effects in loading state, 
// usually used for visual feedback when a page or component is loading data

function Skeleton({
  className,
  ...props
}: React.HTMLAttributes<HTMLDivElement>) {
  return (
    <div
      className={cn("animate-pulse rounded-md bg-muted", className)}
      {...props}
    />
  )
}

export { Skeleton }
