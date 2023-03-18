package lain

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"io/ioutil"
	"mime/multipart"
	"net/http"
	"os"
	"path/filepath"
	"strings"

	"github.com/spf13/cobra"
)

const version = "0.1.0"

func Execute() {
	var rootCmd = &cobra.Command{
		Use: "lain",
	}

	// add
	addCmd := &cobra.Command{
		Use:   "add",
		Short: "Add a Discord channel to manifest",
		Run:   add,
	}
	addCmd.Flags().String("channel", "", "Name of the channel to add")
	addCmd.Flags().String("url", "", "URL to associate with the channel")
	rootCmd.AddCommand(addCmd)

	// delete
	deleteCmd := &cobra.Command{
		Use:   "delete",
		Short: "Delete a Discord channel from manifest",
		Run:   del,
	}
	deleteCmd.Flags().String("channel", "", "Name of the channel to delete")
	rootCmd.AddCommand(deleteCmd)

	// img
	imgCmd := &cobra.Command{
		Use:   "img",
		Short: "Send an image to a Discord channel with optional text",
		Run:   img,
	}
	imgCmd.Flags().String("channel", "", "Name of the channel to send the message")
	imgCmd.Flags().String("msg", "", "Message to send to the channel URL")
	imgCmd.Flags().String("img", "", "Path to the image file to send")
	rootCmd.AddCommand(imgCmd)

	// ls
	lsCmd := &cobra.Command{
		Use:   "ls",
		Short: "List available Discord channels",
		Run:   ls,
	}
	rootCmd.AddCommand(lsCmd)

	// msg
	msgCmd := &cobra.Command{
		Use:   "msg",
		Short: "Send a message to a Discord channel",
		Run:   msg,
	}
	msgCmd.Flags().String("channel", "", "Name of the channel to send the message")
	msgCmd.Flags().String("msg", "", "Message to send to the channel URL")
	rootCmd.AddCommand(msgCmd)

	// version
	versionCmd := &cobra.Command{
		Use:   "version",
		Short: "Print the version of the application",
		Run: func(cmd *cobra.Command, args []string) {
			fmt.Printf("lain version %s\n", version)
		},
	}
	rootCmd.AddCommand(versionCmd)

	rootCmd.Execute()
}

// Add your existing functions here.
func getWebhooksDir() string {
	// Implement your logic to get the webhooks directory
	return "~/.config/sabi/lain/webhooks"
}

func ensureExists(dir string) {
	if _, err := os.Stat(dir); os.IsNotExist(err) {
		os.MkdirAll(dir, os.ModePerm)
	}
}

func add(cmd *cobra.Command, args []string) {
	channel, _ := cmd.Flags().GetString("channel")
	url, _ := cmd.Flags().GetString("url")

	webhooksDir := getWebhooksDir()
	webhooksFile := filepath.Join(webhooksDir, "webhooks")
	ensureExists(webhooksDir)

	webhooks := make(map[string]string)

	if _, err := os.Stat(webhooksFile); !os.IsNotExist(err) {
		data, _ := ioutil.ReadFile(webhooksFile)
		json.Unmarshal(data, &webhooks)
	}

	webhooks[channel] = url

	data, _ := json.Marshal(webhooks)
	ioutil.WriteFile(webhooksFile, data, 0644)

	fmt.Printf("Added %s with URL %s to webhooks.\n", channel, url)
}

func del(cmd *cobra.Command, args []string) {
	dchannel, _ := cmd.Flags().GetString("channel")

	webhooksDir := getWebhooksDir()
	webhooksFile := filepath.Join(webhooksDir, "webhooks")
	ensureExists(webhooksDir)

	webhooks := make(map[string]string)

	if _, err := os.Stat(webhooksFile); !os.IsNotExist(err) {
		data, _ := ioutil.ReadFile(webhooksFile)
		json.Unmarshal(data, &webhooks)
	}

	if _, ok := webhooks[dchannel]; ok {
		delete(webhooks, dchannel)
		data, _ := json.Marshal(webhooks)
		ioutil.WriteFile(webhooksFile, data, 0644)
		fmt.Printf("Deleted %s from webhooks.\n", dchannel)
	} else {
		fmt.Printf("%s not found in webhooks.\n", dchannel)
	}
}

func img(cmd *cobra.Command, args []string) {
	channel, _ := cmd.Flags().GetString("channel")
	msg, _ := cmd.Flags().GetString("msg")
	img, _ := cmd.Flags().GetString("img")

	webhooksDir := getWebhooksDir()
	webhooksFile := filepath.Join(webhooksDir, "webhooks")
	ensureExists(webhooksDir)

	imgPath := filepath.Clean(img)

	if _, err := os.Stat(webhooksFile); os.IsNotExist(err) {
		fmt.Println("No webhooks found.")
		return
	}

	webhooksBytes, _ := ioutil.ReadFile(webhooksFile)
	var webhooks map[string]string
	json.Unmarshal(webhooksBytes, &webhooks)

	if url, ok := webhooks[channel]; ok {
		err := sendImage(url, imgPath, msg)
		if err != nil {
			fmt.Printf("Failed to send image to %s: %v\n", channel, err)
		} else {
			fmt.Printf("Sent image to %s: %s\n", channel, imgPath)
		}
	} else {
		fmt.Printf("%s not found in webhooks.\n", channel)
	}
}

func ls(cmd *cobra.Command, args []string) {
	webhooksDir := getWebhooksDir()
	webhooksFile := filepath.Join(webhooksDir, "webhooks")
	ensureExists(webhooksDir)

	if _, err := os.Stat(webhooksFile); os.IsNotExist(err) {
		fmt.Println("No webhooks found.")
		return
	}

	data, _ := ioutil.ReadFile(webhooksFile)
	webhooks := make(map[string]string)
	json.Unmarshal(data, &webhooks)

	channels := make([]string, 0, len(webhooks))
	for k := range webhooks {
		channels = append(channels, k)
	}

	fmt.Printf("Channels: %s\n", strings.Join(channels, ", "))
}

func msg(cmd *cobra.Command, args []string) {
	channel, _ := cmd.Flags().GetString("channel")
	msg, _ := cmd.Flags().GetString("msg")

	webhooksDir := getWebhooksDir()
	webhooksFile := filepath.Join(webhooksDir, "webhooks")
	ensureExists(webhooksDir)

	if _, err := os.Stat(webhooksFile); os.IsNotExist(err) {
		fmt.Println("No webhooks found.")
		return
	}

	webhooksBytes, _ := ioutil.ReadFile(webhooksFile)
	var webhooks map[string]string
	json.Unmarshal(webhooksBytes, &webhooks)

	if url, ok := webhooks[channel]; ok {
		resp, err := http.Post(url, "application/json", strings.NewReader(fmt.Sprintf(`{"content": "%s"}`, msg)))
		if err != nil {
			fmt.Printf("Failed to send message to %s: %v\n", channel, err)
			return
		}
		defer resp.Body.Close()

		if resp.StatusCode >= 200 && resp.StatusCode < 300 {
			fmt.Printf("Sent message to %s: %s\n", channel, msg)
		} else {
			fmt.Printf("Failed to send message to %s: status code %d\n", channel, resp.StatusCode)
		}
	} else {
		fmt.Printf("%s not found in webhooks.\n", channel)
	}
}

func sendImage(url, imgPath, msg string) error {
	file, err := os.Open(imgPath)
	if err != nil {
		return err
	}
	defer file.Close()

	body := &bytes.Buffer{}
	writer := multipart.NewWriter(body)

	part, err := writer.CreateFormFile("file", filepath.Base(imgPath))
	if err != nil {
		return err
	}
	_, err = io.Copy(part, file)

	err = writer.WriteField("content", msg)
	if err != nil {
		return err
	}

	err = writer.Close()
	if err != nil {
		return err
	}

	req, err := http.NewRequest("POST", url, body)
	if err != nil {
		return err
	}

	req.Header.Set("Content-Type", writer.FormDataContentType())

	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		return err
	}
	defer resp.Body.Close()

	if resp.StatusCode < 200 || resp.StatusCode >= 300 {
		return fmt.Errorf("non-2xx status code: %d", resp.StatusCode)
	}

	return nil
}
