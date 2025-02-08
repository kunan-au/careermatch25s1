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
import { useResumeUpdate } from "./useResumeUpdate";
import { useState } from "react";

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
  const { user_profile } = useUser();
  const { email } = user_profile ? user_profile : { email: "user@example.com" };

  const { user_info } = useProfile(email);
  const { name, avatar, resume } = user_info || defaultInfoData;

  const { profileUpdate } = useProfileUpdate();

  const { updateAvatar } = useAvatarUpdate();

  const { updateResume } = useResumeUpdate();

  const [resumeFile, setResumeFile] = useState<File | null>(null);

  const handleResumeChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files[0]) {
      setResumeFile(event.target.files[0]);
    }
  };

  const handleResumeSubmit = async (
    event: React.FormEvent<HTMLFormElement>
  ) => {
    event.preventDefault();
    if (resumeFile) {
      await updateResume({ email, file: resumeFile });
    }
  };

  const handleUpdateAvatar = async (
    event: React.FormEvent<HTMLFormElement>
  ) => {
    event.preventDefault();
    const formData = new FormData(event.currentTarget);
    const file = formData.get("avatar") as File;

    await updateAvatar({ email, file });
  };

  const handleSubmitProfile = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const formData = new FormData(event.currentTarget);
    console.log(formData);
    const userData: UserData = {
      email,
      name: formData.get("name") as string,
      avatar,
      resume,
    };
    profileUpdate(userData);
  };

  return (
    <div className="text-center bg-gray-50">
      <h1 className="w-full text-center text-3xl font-bold py-10">
        {name ? name : "Anonymous"}
      </h1>

      <div className="flex items-center justify-center gap-20 max-[950px]:flex-col">
        <div className="flex flex-col gap-10 items-center">
          <div className="bg-white overflow-hidden shadow rounded-lg border h-96">
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
                      Choose your new avatar here. Click save when you're done.
                      Acceptable image formats include JPG, JPEG, PNG.
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
                <h3 className="text-lg leading-6 font-medium text-gray-900">
                  Your Profile
                </h3>
                <p className="mt-1 max-w-2xl text-sm text-gray-500">
                  This is the basic information you provided.
                </p>
              </div>
            </div>
            <div className="border-t border-gray-200 px-4 py-5 sm:p-0">
              <dl className="sm:divide-y sm:divide-gray-200">
                <div className="py-3 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                  <dt className="text-sm font-medium text-gray-500">Name</dt>
                  <dd className="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                    {name ? name : "Anonymous"}
                  </dd>
                </div>
                <div className="py-3 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                  <dt className="text-sm font-medium text-gray-500">
                    Email address
                  </dt>
                  <dd className="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                    {email}
                  </dd>
                </div>
                <div className="py-3 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                  <dt className="text-sm font-medium text-gray-500">
                    Phone number
                  </dt>
                  <dd className="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                    +61 0123456789
                  </dd>
                </div>
                <div className="py-3 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                  <dt className="text-sm font-medium text-gray-500">Address</dt>
                  <dd className="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                    108 North Rd, Acton ACT 2601
                  </dd>
                </div>
              </dl>
            </div>
          </div>

          <Dialog>
            <DialogTrigger asChild>
              <Button variant="outline" className="mb-5 mx-auto">
                Edit Profile
              </Button>
            </DialogTrigger>
            <DialogContent className="sm:max-w-[425px]">
              <DialogHeader>
                <DialogTitle>Edit profile</DialogTitle>
                <DialogDescription>
                  Make changes to your profile here. Click save when you're
                  done.
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
                      type="text"
                      defaultValue={name ? name : "Anonymous"}
                      className="col-span-3"
                    />
                  </div>
                  <div className="grid grid-cols-4 items-center gap-4">
                    <Label htmlFor="phone" className="text-right">
                      Phone Number
                    </Label>
                    <Input
                      id="phone"
                      name="phone"
                      type="text"
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
                      type="text"
                      defaultValue="Acton ACT, 2601"
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

        <div className="flex flex-col gap-10 items-center">
          <div>
            <div className="overflow-hidden rounded-lg shadow">
              <iframe
                src={
                  resume
                    ? `https://careermatch-resume-2024.s3.ap-southeast-2.amazonaws.com/${resume}`
                    : "./sample-resume.pdf"
                }
                // src="./sample-resume.pdf"
                className="w-full h-96"
              ></iframe>
            </div>
          </div>

          <Dialog>
            <DialogTrigger asChild>
              <Button variant="outline" className="mb-5 mx-auto">
                Update Resume
              </Button>
            </DialogTrigger>
            <DialogContent className="sm:max-w-[425px]">
              <DialogHeader>
                <DialogTitle>Update Resume</DialogTitle>
                <DialogDescription>
                  Upload your latest resume here. Only PDF files are accepted.
                  Click save when you're done.
                </DialogDescription>
              </DialogHeader>
              <form onSubmit={handleResumeSubmit}>
                <div className="grid gap-4 py-4">
                  <div className="grid grid-cols-4 items-center gap-4">
                    <Label htmlFor="resume" className="text-right">
                      New Resume
                    </Label>
                    <Input
                      type="file"
                      id="resume"
                      onChange={handleResumeChange}
                      accept="application/pdf"
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
      </div>
    </div>
  );
}
