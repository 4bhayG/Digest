import { google } from "googleapis";

// Replace with your API key or OAuth2 credentials
const API_KEY = "AIzaSyCI-qtvjLHFbSsiHUQ6DSwwpOoF9ltQLhg" ;
const oAuthKey = "96619426130-gfbd0vta53g1cepemj6ohd7vqn8oas94.apps.googleusercontent.com";

const VIDEO_ID = "GGi7Brsf7js"; // Replace with the YouTube video ID

// Initialize the YouTube API client
const youtube = google.youtube({
  version: "v3",
  auth: API_KEY,
});

// Function to list captions for a video
async function listCaptions() {
  try {
    const response = await youtube.captions.list({
      part: "snippet",
      videoId: VIDEO_ID,
    });

    const captions = response.data.items;
    if (captions.length === 0) {
      console.log("No captions found for this video.");
      return;
    }

    console.log("Captions:");
    captions.forEach((caption, index) => {
      console.log(`${index + 1}. ID: ${caption.id}, Language: ${caption.snippet.language}, Status: ${caption.snippet.status}`);
    });

    // Download the first caption (you can modify this to download a specific caption)
    if (captions.length > 0) {
      const captionId = captions[0].id;
      await downloadCaption(captionId);
    }
  } catch (error) {
    console.error("Error listing captions:", error.message);
  }
}

// Function to download a caption
async function downloadCaption(captionId) {
  try {
    const response = await youtube.captions.download({
      id: captionId,
      tfmt: "srt", // SubRip format (you can use 'vtt' for WebVTT)
      tlang: "en", // Optional: specify language
    });

    console.log("Caption content:");
    console.log(response.data); // The caption content
  } catch (error) {
    console.error("Error downloading caption:", error.message);
  }
}

// Run the function
listCaptions();