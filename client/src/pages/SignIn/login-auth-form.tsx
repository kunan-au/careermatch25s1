import { cn } from "@/lib/utils";
// import { Icons } from "@/components/ui/icons";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { useLogin } from "./useLogin";
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

interface UserAuthFormProps extends React.HTMLAttributes<HTMLDivElement> {}

export function LoginAuthForm({ className, ...props }: UserAuthFormProps) {
  const navigate = useNavigate();
  const { status, login } = useLogin();
  const [role, setRole] = useState<"recruiter" | "candidate">("candidate");

  useEffect(() => {
    if (status === "success") {
      const storedRole = localStorage.getItem("role");
      setTimeout(() => {
        if (storedRole === "recruiter") {
          navigate("/post");
        } else {
          navigate("/jobs");
        }
      }, 1000);
    }
  }, [status, navigate]);

  async function onSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();

    const email = event.currentTarget.email.value;
    const password = event.currentTarget.password.value;

    localStorage.setItem("role", role); // ✅ Save role to localStorage
    login({ email, password, role });   // ✅ Send role to backend if needed
  }

  return (
    <div className={cn("grid gap-6", className)} {...props}>
      <form onSubmit={onSubmit}>
        <div className="grid gap-2">
          <div className="grid gap-1">
            <Label htmlFor="role">Sign in as</Label>
            <select
              id="role"
              name="role"
              className="border border-gray-300 rounded-md p-2"
              value={role}
              onChange={(e) => setRole(e.target.value as "recruiter" | "candidate")}
            >
              <option value="candidate">Candidate</option>
              <option value="recruiter">Recruiter</option>
            </select>
          </div>

          <div className="grid gap-1">
            <Label className="sr-only" htmlFor="email">
              Email
            </Label>
            <Input
              id="email"
              name="email"
              placeholder="name@example.com"
              type="email"
              autoCapitalize="none"
              autoComplete="email"
              autoCorrect="off"
            />
          </div>

          <div className="grid gap-1">
            <Label className="sr-only" htmlFor="password">
              Password
            </Label>
            <Input
              id="password"
              name="password"
              placeholder="enter your password"
              type="password"
              autoCapitalize="none"
              autoComplete="current-password"
              autoCorrect="off"
            />
          </div>

          <Button className="mt-10">
            Sign In with Email
          </Button>
        </div>
      </form>
    </div>
  );
}
