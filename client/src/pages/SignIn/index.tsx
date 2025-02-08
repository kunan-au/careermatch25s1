import { Link } from "react-router-dom";
import { LoginAuthForm } from "@/pages/SignIn/login-auth-form";
import { cn } from "@/lib/utils";
import { buttonVariants } from "@/components/ui/button";

export default function SignIn() {
  return (
    <>
      <Link
        to="/signUp"
        className={cn(
          buttonVariants({ variant: "ghost" }),
          "absolute right-4 top-4 md:right-8 md:top-8"
        )}
      >
        Sign Up
      </Link>
      <div className="lg:p-8">
        <div className="mx-auto flex w-full flex-col justify-center space-y-6 sm:w-[350px]">
          <div className="flex flex-col space-y-2 text-center mb-8">
            <h1 className="text-2xl font-semibold tracking-tight">
              Welcome to Career Match
            </h1>
            <p className="text-sm text-muted-foreground">
              Enter your email and password below to sign in
            </p>
          </div>
          <LoginAuthForm />
          <p className="px-8 text-center text-sm text-muted-foreground">
            By clicking continue, you agree to our{" "}
            <Link
              to={"/terms-of-service"}
              className="underline underline-offset-4 hover:text-primary"
            >
              Terms of Service
            </Link>{" "}
            and{" "}
            <Link
              to={"/privacy-policy"}
              className="underline underline-offset-4 hover:text-primary"
            >
              Privacy Policy
            </Link>
            .
          </p>
        </div>
      </div>
    </>
  );
}
