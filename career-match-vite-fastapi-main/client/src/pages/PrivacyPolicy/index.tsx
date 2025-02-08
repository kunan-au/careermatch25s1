import { Button } from "@/components/ui/button";
import { useNavigate } from "react-router-dom";

export default function PrivacyPolicy() {
  const navigate = useNavigate();

  return (
    <div className="mx-10 min-[1000px]:mx-auto max-w-[1000px] mt-10">
      <h1 className="text-2xl font-semibold tracking-tight text-center mb-10">
        Privacy Policy for Career Match
      </h1>
      <p className="text-sm text-muted-foreground text-center">
        Effective Date: March 13, 2024
      </p>
      <h3 className="text-lg font-semibold tracking-tight mt-5">
        Introduction
      </h3>
      <p className="mb-5">
        Welcome to Career Match. We are committed to protecting the privacy of
        our users. This Privacy Policy explains how we collect, use, disclose,
        and safeguard your information when you visit our website.
      </p>
      <h3 className="text-lg font-semibold tracking-tight mt-5">
        Information Collection
      </h3>
      <p className="mb-5">
        We collect personal information when you register, log in, submit a
        resume, or apply for jobs. This information may include but is not
        limited to your name, email address, phone number, and employment
        history.
      </p>
      <h3 className="text-lg font-semibold tracking-tight mt-5">
        Use of Information
      </h3>
      <p className="mb-5">
        The information we collect is used to provide, maintain, and improve our
        services, communicate with you, respond to inquiries, and for other
        business purposes.
      </p>
      <h3 className="text-lg font-semibold tracking-tight mt-5">
        Cookies and Tracking Technologies
      </h3>
      <p className="mb-5">
        We use cookies and similar tracking technologies to track the activity
        on our website and store certain information. This tracking is done to
        enhance the user experience and understand how our website is used.
      </p>
      <h3 className="text-lg font-semibold tracking-tight mt-5">
        Data Security
      </h3>
      <p className="mb-5">
        We implement a variety of security measures to maintain the safety of
        your personal information. However, no method of transmission over the
        internet is entirely secure.
      </p>
      <h3 className="text-lg font-semibold tracking-tight mt-5">
        Sharing of Information
      </h3>
      <p className="mb-5">
        We do not sell, trade, or otherwise transfer your personally
        identifiable information to outside parties except when we believe
        release is appropriate to comply with the law, enforce our site
        policies, or protect ours or others' rights, property, or safety.
      </p>
      <h3 className="text-lg font-semibold tracking-tight mt-5">
        Third-Party Links
      </h3>
      <p className="mb-5">
        Occasionally, at our discretion, we may include or offer third-party
        products or services on our website. These third-party sites have
        separate and independent privacy policies.
      </p>
      <h3 className="text-lg font-semibold tracking-tight mt-5">
        Children’s Privacy
      </h3>
      <p className="mb-5">
        Our website is not intended for children under the age of 13, and we do
        not knowingly collect personal information from children under 13.
      </p>
      <h3 className="text-lg font-semibold tracking-tight mt-5">
        Your Consent
      </h3>
      <p className="mb-5">
        By using our site, you consent to our website's privacy policy.
      </p>
      <h3 className="text-lg font-semibold tracking-tight mt-5">
        Changes to our Privacy Policy
      </h3>
      <p className="mb-5">
        We reserve the right to update this Privacy Policy at any time. We will
        notify you of any changes by posting the new Privacy Policy on this
        page.
      </p>
      <h3 className="text-lg font-semibold tracking-tight mt-5">Contact Us</h3>
      <p className="mb-5">
        If you have any questions about this Privacy Policy, please contact us
        at [Your Contact Information].
      </p>
      <Button onClick={() => navigate(-1)} className="my-10">
        Back
      </Button>
    </div>
  );
}
