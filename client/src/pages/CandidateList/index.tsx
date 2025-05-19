import { Button } from "@/components/ui/button";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { Card, CardContent } from "@/components/ui/card";

const fakeApplicants = [
  {
    name: "Liam Turner",
    title: "Full Stack Developer",
    appliedTo: "Senior Web Developer",
  },
  {
    name: "Natalie Brooks",
    title: "UI/UX Designer",
    appliedTo: "Product Designer",
  },
  {
    name: "Jason Patel",
    title: "Data Scientist",
    appliedTo: "AI/ML Researcher",
  },
  {
    name: "Grace Lin",
    title: "Mobile Developer",
    appliedTo: "iOS Developer",
  },
  {
    name: "Ethan Wright",
    title: "Cloud Engineer",
    appliedTo: "AWS Solutions Architect",
  },
];

export default function CandidateList() {
  // 提取名字首字母（如 Grace Lin → GL）
  const getInitials = (name: string) => {
    return name
      .split(" ")
      .slice(0, 2)
      .map((part) => part[0])
      .join("")
      .toUpperCase();
  };

  return (
    <>
      <h1 className="w-full text-center text-3xl font-bold py-10 bg-gray-50">
        Candidate List
      </h1>

      <div className="bg-gray-50 pb-10 px-4 lg:px-40">
        <section>
          <h2 className="text-2xl font-semibold mb-6">Applicants</h2>
          <div className="grid gap-4 grid-cols-1">
            {fakeApplicants.map((user, index) => (
              <Card key={index}>
                <CardContent className="flex justify-between items-center p-4">
                  <div className="flex items-center gap-x-6">
                    <Avatar>
                      <AvatarFallback className="font-bold text-xl tracking-wide">
                        {getInitials(user.name)}
                      </AvatarFallback>
                    </Avatar>
                    <div className="flex flex-col">
                      <span className="font-medium">{user.name}</span>
                      <span className="text-muted-foreground text-sm">
                        {user.title}
                      </span>
                      <span className="text-sm text-gray-600">
                        Applied for: {user.appliedTo}
                      </span>
                    </div>
                  </div>
                  <Button size="sm">View Detail</Button>
                </CardContent>
              </Card>
            ))}
          </div>
        </section>
      </div>
    </>
  );
}
