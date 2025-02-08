import { Button } from "@/components/ui/button";
import { useNavigate } from "react-router-dom";

export default function TermsOfService() {
  const navigate = useNavigate();

  return (
    <div className="mx-10 min-[1000px]:mx-auto max-w-[1000px] mt-10">
      <h1 className="text-2xl font-semibold tracking-tight text-center mb-10">
        Terms of Service for Career Match
      </h1>
      <p className="text-sm text-muted-foreground text-center">
        Last Updated: March 13, 2024
      </p>
      <h3 className="text-lg font-semibold tracking-tight mt-5">
        1. Introduction
      </h3>
      <p className="mb-5">
        Welcome to Career Match. By accessing our website and using our
        services, you agree to comply with these Terms of Service.
      </p>
      <h3 className="text-lg font-semibold tracking-tight mt-5">
        2. User Obligations
      </h3>
      <p className="mb-5">
        Users must provide accurate and current information during registration
        and job application processes. Misuse or unauthorized use of our website
        and its features is strictly prohibited.
      </p>
      <h3 className="text-lg font-semibold tracking-tight mt-5">
        3. Intellectual
      </h3>
      <p className="mb-5">
        Property Rights All content on our website, including text, graphics,
        logos, and images, is the property of Career Match and is protected by
        intellectual property laws.
      </p>
      <h3 className="text-lg font-semibold tracking-tight mt-5">
        4. User-Generated Content
      </h3>
      <p className="mb-5">
        Users are responsible for any content they post or submit, including but
        not limited to job listings and resumes. Content should not infringe on
        the rights of others or contain harmful or illegal material.
      </p>
      <h3 className="text-lg font-semibold tracking-tight mt-5">
        5. Privacy Policy
      </h3>
      <p className="mb-5">
        Our Privacy Policy, which details how we handle user data, is an
        integral part of these Terms of Service.
      </p>
      <h3 className="text-lg font-semibold tracking-tight mt-5">
        6. Limitation of Liability
      </h3>
      <p className="mb-5">
        Career Match will not be liable for any damages resulting from the use
        of our website or services.
      </p>
      <h3 className="text-lg font-semibold tracking-tight mt-5">
        7. Changes to Terms of Service
      </h3>
      <p className="mb-5">
        We reserve the right to modify these Terms of Service at any time.
        Continued use of our services after changes signifies acceptance of the
        new terms.
      </p>
      <h3 className="text-lg font-semibold tracking-tight mt-5">
        8. Governing Law
      </h3>
      <p className="mb-5">
        These Terms of Service are governed by the laws of Australia. 9. Contact
        Information For any inquiries or complaints regarding the service or
        terms, users can contact us at [Your Contact Information].
      </p>
      <Button onClick={() => navigate(-1)} className="my-10">
        Back
      </Button>
    </div>
  );
}
