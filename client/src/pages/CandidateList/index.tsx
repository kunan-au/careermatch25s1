import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Avatar, AvatarImage, AvatarFallback } from "@/components/ui/avatar";
import { Card, CardContent } from "@/components/ui/card";

const fakeApplicants = [
  {
    name: "Alice Johnson",
    title: "Frontend Developer",
    appliedTo: "Frontend Role",
  },
  {
    name: "Michael Lee",
    title: "Product Manager",
    appliedTo: "PM Role",
  },
  {
    name: "Emily Chen",
    title: "Backend Engineer",
    appliedTo: "Backend Role",
  },
  {
    name: "John Smith",
    title: "DevOps Engineer",
    appliedTo: "DevOps Role",
  },
  {
    name: "Sophia Davis",
    title: "Software Engineer",
    appliedTo: "Graduate SWE",
  },
];

export default function CandidateList() {
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
                      <AvatarImage src={`https://i.pravatar.cc/80?u=${user.name}`} />
                      <AvatarFallback>{user.name.charAt(0)}</AvatarFallback>
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
