import { Component } from '@angular/core';
import { UploadPreviewComponent } from '../upload-preview/upload-preview.component';
import { NgIf } from '@angular/common';

interface FileSchemaTable {
  id: number,
  fileName: string,
  fileType: string,
  fileSize: number,
  file: File,
  fileExtention: string,
}

@Component({
  selector: 'app-dashboard',
  imports: [UploadPreviewComponent, NgIf],
  templateUrl: './dashboard.component.html',
  styleUrl: './dashboard.component.css',
})
export class DashboardComponent {
  isDragging = false;
  showUploadPreview = false
  uploadedFiles: FileSchemaTable[] = []
  supportedFileFormats = ["png", "jpg"]

  onDragOver(event: DragEvent) {
    event.preventDefault();
    this.isDragging = true;
  }

  onDragLeave(event: DragEvent) {
    event.preventDefault();
    this.isDragging = false;
  }

  onDrop(event: DragEvent) {
    event.preventDefault();
    this.isDragging = false;
    const files = event.dataTransfer?.files;
    if (!files || files.length === 0) return;
    this.handleFiles(files);
  }

  onFileSelect(event: Event) {
    const input = event.target as HTMLInputElement | null;
    const files = input?.files;
    if (!files || files.length === 0) return;

    this.handleFiles(files);
  }

  handleFiles(files: FileList) {
    for (let i = 0; i < files.length; i++) {
      try {
        const file = files.item(i);
        const data: FileSchemaTable = {
          id: i,
          fileName: file!.name,
          fileSize: file!.size,
          fileType: file!.type,
          fileExtention: file!.name.split('.').pop()!,
          file: file!,
        };
        this.uploadedFiles.push(data)
        this.showUploadPreview = true
      } catch (err) {
        console.log("Wrong File uploaded");
      }
      console.log(this.uploadedFiles);
    }
  }

  closePreviewButton() {
    this.uploadedFiles = []
    this.showUploadPreview = false
  }
}
