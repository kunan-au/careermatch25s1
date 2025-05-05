import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
  DialogClose,
} from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { useProfile } from "./useProfile";
import { useUser } from "../SignIn/useUser";
import { useProfileUpdate } from "./useProfileUpdate";
import { useAvatarUpdate } from "./useAvatarUpdate";
import { useEffect, useState } from "react";

const defaultInfoData = {
  email: "string",
  name: "string",
  avatar: "string",
  resume: "string",
};

type UserData = {
  email: string;
  name: string;
  avatar: string;
  resume: string;
};

export default function ProfileInfo() {
  const role = localStorage.getItem("role") || "candidate"; // ✅ 读取角色
  const { user_profile } = useUser();
  const { email } = user_profile ? user_profile : { email: "user@example.com" };

  const { user_info } = useProfile(email);
  const { name, avatar, resume } = user_info || defaultInfoData;

  const { profileUpdate } = useProfileUpdate();
  const { updateAvatar } = useAvatarUpdate();

  const [resumePreview, setResumePreview] = useState<string | null>(null);

  const defaultResumeURL = "/sample-resume.pdf";

  useEffect(() => {
    const storedPreview = localStorage.getItem("resumePreview");
    if (storedPreview) {
      setResumePreview(storedPreview);
    }
  }, []);

  const handleResumeChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files[0]) {
      const file = event.target.files[0];
      const previewURL = URL.createObjectURL(file);
      setResumePreview(previewURL);
      localStorage.setItem("resumePreview", previewURL);
    }
  };

  const handleUpdateAvatar = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const formData = new FormData(event.currentTarget);
    const file = formData.get("avatar") as File;
    await updateAvatar({ email, file });
  };

  const handleSubmitProfile = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const formData = new FormData(event.currentTarget);

    const userData: UserData = {
      email,
      name: formData.get("name") as string,
      avatar,
      resume,
    };
    profileUpdate(userData);
  };

  return (
    <div className="text-center bg-gray-50 min-h-screen py-10">
      <h1 className="text-3xl font-bold mb-10">
        {name ? name : "Anonymous"}
      </h1>

      <div
        className={`flex justify-center gap-20 max-[950px]:flex-col ${
          role === "recruiter" ? "items-center" : ""
        }`}
      >
        {/* Left side: Avatar and info */}
        <div
          className={`flex flex-col gap-10 ${
            role === "recruiter" ? "items-center w-[500px]" : "items-center"
          }`}
        >
          <div className="bg-white overflow-hidden shadow rounded-lg border h-96 w-full">
            <div className="px-4 py-7 sm:px-6 flex items-center gap-5">
              <Dialog>
                <DialogTrigger>
                  <Avatar className="h-20 w-20">
                    <AvatarImage
                      src={
                        avatar
                          ? `https://careermatch-avatar-2024.s3.ap-southeast-2.amazonaws.com/${avatar}`
                          : "https://github.com/shadcn.png"
                      }
                    />
                    <AvatarFallback>CN</AvatarFallback>
                  </Avatar>
                </DialogTrigger>
                <DialogContent className="sm:max-w-[425px]">
                  <DialogHeader>
                    <DialogTitle>Edit Avatar</DialogTitle>
                    <DialogDescription>
                      Choose your new avatar here. Acceptable formats: JPG, PNG.
                    </DialogDescription>
                  </DialogHeader>
                  <form onSubmit={handleUpdateAvatar}>
                    <div className="grid gap-4 py-4">
                      <div className="grid grid-cols-4 items-center gap-4">
                        <Label htmlFor="avatar" className="text-right">
                          New Avatar
                        </Label>
                        <Input
                          type="file"
                          id="avatar"
                          name="avatar"
                          accept="image/*"
                          className="col-span-3"
                        />
                      </div>
                    </div>
                    <DialogFooter>
                      <DialogClose>
                        <Button type="submit">Save changes</Button>
                      </DialogClose>
                    </DialogFooter>
                  </form>
                </DialogContent>
              </Dialog>

              <div>
                <h3 className="text-lg font-medium text-gray-900">
                  Your Profile
                </h3>
                <p className="text-sm text-gray-500">Basic public info</p>
              </div>
            </div>

            <div className="border-t border-gray-200 px-4 py-5 sm:p-0">
              <dl className="sm:divide-y sm:divide-gray-200 text-left">
                <div className="py-3 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                  <dt className="text-sm font-medium text-gray-500">Name</dt>
                  <dd className="text-sm text-gray-900 sm:col-span-2">
                    {name || "Anonymous"}
                  </dd>
                </div>
                <div className="py-3 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                  <dt className="text-sm font-medium text-gray-500">Email</dt>
                  <dd className="text-sm text-gray-900 sm:col-span-2">
                    {email}
                  </dd>
                </div>
                <div className="py-3 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                  <dt className="text-sm font-medium text-gray-500">Phone</dt>
                  <dd className="text-sm text-gray-900 sm:col-span-2">
                    +61 0123456789
                  </dd>
                </div>
                <div className="py-3 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                  <dt className="text-sm font-medium text-gray-500">Address</dt>
                  <dd className="text-sm text-gray-900 sm:col-span-2">
                    108 North Rd, Acton ACT 2601
                  </dd>
                </div>
              </dl>
            </div>
          </div>

          {/* Edit Profile */}
          <Dialog>
            <DialogTrigger asChild>
              <Button variant="outline">Edit Profile</Button>
            </DialogTrigger>
            <DialogContent className="sm:max-w-[425px]">
              <DialogHeader>
                <DialogTitle>Edit Profile</DialogTitle>
                <DialogDescription>
                  Change your profile info. Click save when done.
                </DialogDescription>
              </DialogHeader>
              <form onSubmit={handleSubmitProfile}>
                <div className="grid gap-4 py-4">
                  <div className="grid grid-cols-4 items-center gap-4">
                    <Label htmlFor="name" className="text-right">
                      Name
                    </Label>
                    <Input
                      id="name"
                      name="name"
                      defaultValue={name}
                      className="col-span-3"
                    />
                  </div>
                  <div className="grid grid-cols-4 items-center gap-4">
                    <Label htmlFor="phone" className="text-right">
                      Phone
                    </Label>
                    <Input
                      id="phone"
                      name="phone"
                      defaultValue="+61 0123456789"
                      className="col-span-3"
                    />
                  </div>
                  <div className="grid grid-cols-4 items-center gap-4">
                    <Label htmlFor="address" className="text-right">
                      Address
                    </Label>
                    <Input
                      id="address"
                      name="address"
                      defaultValue="108 North Rd, Acton ACT 2601"
                      className="col-span-3"
                    />
                  </div>
                </div>
                <DialogFooter>
                  <DialogClose>
                    <Button type="submit">Save changes</Button>
                  </DialogClose>
                </DialogFooter>
              </form>
            </DialogContent>
          </Dialog>
        </div>

        {/* Right side: Resume section (only for candidate) */}
        {role === "candidate" && (
          <div className="flex flex-col gap-10 items-center">
            <div className="overflow-hidden rounded-lg shadow w-[400px]">
              {resumePreview || resume ? (
                <iframe
                  src={
                    resumePreview ||
                    `https://careermatch-resume-2024.s3.ap-southeast-2.amazonaws.com/${resume}`
                  }
                  className="w-full h-96"
                ></iframe>
              ) : (
                <div className="w-full h-96 bg-gray-200 flex items-center justify-center">
                  <p className="text-gray-500">No resume uploaded</p>
                </div>
              )}
            </div>

            <Dialog>
              <DialogTrigger asChild>
                <Button variant="outline">Update Resume</Button>
              </DialogTrigger>
              <DialogContent className="sm:max-w-[425px]">
                <DialogHeader>
                  <DialogTitle>Update Resume</DialogTitle>
                  <DialogDescription>
                    Upload a PDF resume. Click save when you're done.
                  </DialogDescription>
                </DialogHeader>
                <form>
                  <div className="grid gap-4 py-4">
                    <div className="grid grid-cols-4 items-center gap-4">
                      <Label htmlFor="resume" className="text-right">
                        Resume
                      </Label>
                      <Input
                        type="file"
                        id="resume"
                        accept="application/pdf"
                        onChange={handleResumeChange}
                        className="col-span-3"
                      />
                    </div>
                  </div>
                  <DialogFooter>
                    <DialogClose>
                      <Button type="button">Save changes</Button>
                    </DialogClose>
                  </DialogFooter>
                </form>
              </DialogContent>
            </Dialog>
          </div>
        )}
      </div>
    </div>
  );
}
