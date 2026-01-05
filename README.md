# WhatsApp Chat Analyzer - Testing

This folder contains test cases and testing utilities for the WhatsApp Chat Analyzer project.

## Project Overview

**WhatsApp Chat Analyzer** is a tool designed to analyze WhatsApp chat exports and provide insights into messaging patterns, user activity, and conversation statistics.

## Testing Structure

This testing folder is organized to ensure comprehensive coverage of the chat analyzer functionality.

### Test Categories

- **Unit Tests:** Test individual functions and components
- **Integration Tests:** Test the interaction between different modules
- **Data Validation Tests:** Ensure proper parsing of WhatsApp chat formats
- **Edge Case Tests:** Handle unusual or malformed chat data

## Test Data

Sample WhatsApp chat exports should be placed in this folder for testing purposes. Ensure all test data:
- Has personal information anonymized
- Covers various chat formats (different WhatsApp versions)
- Includes edge cases (empty messages, media files, deleted messages)

## Running Tests

Instructions for running tests will be added as the testing framework is set up.

```bash
# Example command (update as needed)
python -m pytest tests/
```

## Test Checklist

- [ ] Chat file parsing
- [ ] Date and time extraction
- [ ] User identification
- [ ] Message counting
- [ ] Media detection
- [ ] Emoji analysis
- [ ] Activity patterns
- [ ] Error handling for corrupted files

## Features to Test

1. **Message Statistics**
   - Total message count
   - Messages per user
   - Average message length

2. **Time Analysis**
   - Most active hours
   - Most active days
   - Activity heatmaps

3. **Content Analysis**
   - Most used words
   - Emoji frequency
   - Media sharing patterns

4. **User Insights**
   - Response times
   - Conversation starters
   - Activity comparison
**Author:** B Rohit Kumar  
**CSE Student**  
**Happy Coding!** 🚀
