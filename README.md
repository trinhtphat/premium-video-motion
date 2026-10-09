# Recap Video Archive

Repository này lưu trữ project **Recap Training Reel** và quy trình sản xuất video đã được thống nhất trong cuộc trao đổi ngày 09/10/2026.

## Nội dung chính

- [`VIDEO_PRODUCTION_PLAYBOOK.md`](VIDEO_PRODUCTION_PLAYBOOK.md) — quy trình tái sử dụng cho các yêu cầu video sau này.
- [`AGENTS.md`](AGENTS.md) — nguyên tắc bắt buộc dành cho agent khi nhận yêu cầu tạo video trong repository này.
- [`recap-training-reel/`](recap-training-reel/) — source HyperFrames của video recap 15 giây, 9:16.
- [`recap-training-reel/BRIEF.md`](recap-training-reel/BRIEF.md) — creative brief đã chốt.
- [`recap-training-reel/frame.md`](recap-training-reel/frame.md) — design system “Electric Editorial”.
- [`recap-training-reel/STORYBOARD.md`](recap-training-reel/STORYBOARD.md) — storyboard 6 cảnh.

## Trạng thái project

- Source video đã hoàn thiện và vượt qua HyperFrames check tại thời điểm lưu.
- Studio preview: `http://localhost:3003/#project/recap-training-reel` khi preview server đang chạy.
- Chưa render MP4 cuối vì quy trình yêu cầu người dùng duyệt preview trước khi render.

## Chạy lại project

```powershell
cd recap-training-reel
npm run check
npx --yes hyperframes@0.8.143 preview --background
```

Sau khi duyệt preview:

```powershell
npm run render
```
