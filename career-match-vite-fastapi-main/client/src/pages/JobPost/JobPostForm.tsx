import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { z } from "zod";
import { useEffect } from "react";

import { Button } from "@/components/ui/button";
import {
  Form,
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Textarea } from "@/components/ui/textarea";

import { useJobPost } from "./useJobpost";

const formSchema = z.object({
  title: z.string().min(1, {
    message: "Job title is required.",
  }),
  company: z.string().min(1, {
    message: "Company name is required.",
  }),
  job_type: z.enum(["ft", "pt", "cv", "ct"]),
  description: z.string().min(1, {
    message: "Job description is required.",
  }),
});

export function JobPostForm() {
  // Add API here
  const { status, jobPost, responseData } = useJobPost();

  useEffect(() => {
    if (status === "success") {
      console.log(responseData);
    }
  }, [status, responseData]);

  // 1. Define the form.
  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      title: "",
      company: "",
      job_type: "ft",
      description: "",
    },
  });

  // 2. Define a submit handler.
  function onSubmit(values: z.infer<typeof formSchema>) {
    console.log(values);
    jobPost(values);
    // reset the form value
    form.reset({
      title: "",
      company: "",
      job_type: "ft",
      description: "",
    });
  }

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-8">
        <FormField
          control={form.control}
          name="title"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Job Title</FormLabel>
              <FormControl>
                <Input placeholder="Enter your job title here" {...field} />
              </FormControl>
              <FormDescription>
                Enter the official title for the position. This will be
                displayed prominently in the job listing.
              </FormDescription>
              <FormMessage />
            </FormItem>
          )}
        />

        <FormField
          control={form.control}
          name="company"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Company</FormLabel>
              <FormControl>
                <Input placeholder="Enter company name here" {...field} />
              </FormControl>
              <FormDescription>
                Provide the name of the company or organization offering the
                position.
              </FormDescription>
              <FormMessage />
            </FormItem>
          )}
        />

        <FormField
          control={form.control}
          name="job_type"
          render={({ field: { onChange, value, name } }) => (
            <FormItem>
              <FormLabel>Job Type</FormLabel>
              <FormControl>
                <Select name={name} onValueChange={onChange} value={value}>
                  <SelectTrigger className="w-[180px]">
                    <SelectValue placeholder="Select a Type" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="ft">Full Time</SelectItem>
                    <SelectItem value="pt">Part time</SelectItem>
                    <SelectItem value="cv">Casual/Vacation</SelectItem>
                    <SelectItem value="ct">Contract/Temp</SelectItem>
                  </SelectContent>
                </Select>
              </FormControl>
              <FormDescription>
                Select the employment classification that best describes the
                nature of the job.
              </FormDescription>
              <FormMessage />
            </FormItem>
          )}
        />

        <FormField
          control={form.control}
          name="description"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Job Description</FormLabel>
              <FormControl>
                <Textarea
                  {...field}
                  placeholder="Enter job description here..."
                />
              </FormControl>
              <FormDescription>
                Detail the responsibilities, duties, and qualifications for the
                role. Be clear and concise to attract the best candidates.
              </FormDescription>
              <FormMessage />
            </FormItem>
          )}
        />

        <Button type="submit">Publish</Button>
      </form>
    </Form>
  );
}
