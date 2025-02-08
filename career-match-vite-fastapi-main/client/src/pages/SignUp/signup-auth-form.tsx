import { useNavigate } from "react-router-dom";
import { useEffect } from "react";
import { useForm, SubmitHandler } from "react-hook-form";

import { cn } from "@/lib/utils";
// import { Icons } from "@/components/ui/icons";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { useRegister } from "./useRegister";

interface UserAuthFormProps extends React.HTMLAttributes<HTMLDivElement> {}

type FormValues = {
  email: string;
  password: string;
  rePassword: string;
};

export function SignUpAuthForm({ className, ...props }: UserAuthFormProps) {
  const { status, register } = useRegister();
  const navigate = useNavigate();

  // react hoot form
  const {
    register: registerForm,
    handleSubmit,
    getValues,
    formState: { errors },
  } = useForm<FormValues>();

  useEffect(() => {
    if (status === "success") {
      setTimeout(() => {
        navigate("/");
      }, 1000);
    }
  }, [status, navigate]);

  const onSubmit: SubmitHandler<FormValues> = (data) => {
    console.log(data);
    const { email, password } = data;
    register({ email, password });
  };

  return (
    <div className={cn("grid gap-6", className)} {...props}>
      <form onSubmit={handleSubmit(onSubmit)}>
        <div className="grid gap-2">
          <div className="grid gap-1">
            <Label htmlFor="email">Email</Label>
            <Input
              id="email"
              placeholder="name@example.com"
              type="email"
              autoCapitalize="none"
              autoComplete="email"
              autoCorrect="off"
              // disabled={status === "loading"}
              {...registerForm("email", {
                required: "Email address is required!",
              })}
            />
            {errors?.email && (
              <p className="text-xs text-rose-500	">{errors.email.message}</p>
            )}
          </div>

          <div className="grid gap-1 mt-5">
            <Label htmlFor="password">Password</Label>
            <Input
              id="password"
              placeholder="enter your password"
              type="password"
              autoCapitalize="none"
              autoComplete="current-password"
              autoCorrect="off"
              // disabled={isLoading}
              {...registerForm("password", {
                required: "Password is required",
                pattern: {
                  value:
                    /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&*]).{8,}$/,
                  message:
                    "Password must contain at least one digit, one uppercase letter, one lowercase letter, one special character of !@#$%^&*, and be at least 8 characters long!",
                },
              })}
            />
            {errors?.password && (
              <p className="text-xs text-rose-500	">{errors.password.message}</p>
            )}
          </div>

          <div className="grid gap-1 mt-5">
            <Label htmlFor="confirm-password">Confirm Password</Label>
            <Input
              id="confirm-password"
              placeholder="confirm your password"
              type="password"
              autoCapitalize="none"
              autoComplete="current-password"
              autoCorrect="off"
              // disabled={isLoading}
              {...registerForm("rePassword", {
                required: "This field is required",
                validate: (value) =>
                  value === getValues().password ||
                  "Your passwords don't match!",
              })}
            />
            {errors?.rePassword && (
              <p className="text-xs text-rose-500	">
                {errors.rePassword.message}
              </p>
            )}
          </div>
          <Button
            // disabled={isLoading}
            className="mt-10"
          >
            {/* {isLoading && (
              <Icons.spinner className="mr-2 h-4 w-4 animate-spin" />
            )} */}
            Create your account
          </Button>
        </div>
      </form>
    </div>
  );
}
