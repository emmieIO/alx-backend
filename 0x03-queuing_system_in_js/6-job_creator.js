import kue from "kue";

const queue = kue.createQueue();

const jobData = {
  phoneNumber: "1234567890",
  message: "This is a test message",
};

const job = queue.create("push_notification_code", jobData).save((err) => {
  if (err) {
    console.error("Error creating job:", err);
  } else {
    console.log(`Notification job created: ${job.id}`);
  }
});

job
  .on("complete", () => {
    console.log("Notification job completed");
  })
  .on("failed", (err) => {
    console.error("Notification job failed:", err);
  });
