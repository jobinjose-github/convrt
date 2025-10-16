import { NgFor, NgClass } from '@angular/common';
import { Component, EventEmitter, Input, Output } from '@angular/core';
import { TruncateMiddlePipe } from "../../shared/pipes/truncate-middle.pipe";
import { KbToMb } from '../../shared/pipes/kb-to-mb.pipe';

interface FileSchemaTable {
  id: number;
  fileName: string,
  fileType: string,
  fileSize: number,
  file: File,
  fileExtention: string,
}

interface FileFormatMap {
  [key: string]: string[];
}

@Component({
  selector: 'app-upload-preview',
  imports: [NgFor, TruncateMiddlePipe, KbToMb, NgClass],
  templateUrl: './upload-preview.component.html',
  styleUrl: './upload-preview.component.css'
})
export class UploadPreviewComponent {
  @Input() fileData: FileSchemaTable[] = [];
  @Output() closePreview: EventEmitter<void> = new EventEmitter();
  selectedFileList: FileSchemaTable[] = [];

  sourceFileMap: FileFormatMap = {
    png: [
      "jpg",
      "svg",
      "webp"
    ],
    jpg: [
      "png",
      "svg",
      "webp"
    ],
    svg: [
      "png",
      "jpg",
      "webp"
    ],
    webp: [
      "png",
      "jpg"
    ]
  }
  sourceType: string[] = []
  sourceFileOptions: string[] = []
  selectedSourceFileType: string = ''
  destFileOptions: string[] = []
  selectedDestFileType: string = ""

  ngOnInit() {
    this.fileData = this.fileData.filter(item => Object.keys(this.sourceFileMap).includes((item.fileExtention).toLowerCase())).map(item => item);
    this.sourceType = this.fileData.map(item => item.fileExtention.toLowerCase());
    this.sourceFileOptions = [...new Set(this.sourceType)];
    this.selectedSourceFileType = this.sourceFileOptions[0];
    this.destFileOptions = this.sourceFileMap[this.selectedSourceFileType]
    this.selectedDestFileType = ""
    this.selectedFileList = this.filterSelectedTypeFiles(this.selectedSourceFileType)
  }

  filterSelectedTypeFiles(selectedSourceFileType: string) {
    return this.fileData.filter(item => item.fileExtention.toLowerCase() == selectedSourceFileType)
  }

  onSelectionChange(event: any) {
    if (event.target.id == "source-type") {
      this.selectedSourceFileType = event.target.value;
      this.destFileOptions = this.sourceFileMap[this.selectedSourceFileType];
      this.selectedFileList = this.filterSelectedTypeFiles(this.selectedSourceFileType)
    } else if (event.target.id == "dest-type") {
      this.selectedDestFileType = event.target.value;
    }
  }

  isFileSelected(fileId: number): boolean {
    return this.selectedFileList.some(f => f.id === fileId);
  }


  convertFile() {
    const data = {
      "source_type": this.selectedSourceFileType,
      "dest_type": this.selectedDestFileType,
      "files": this.selectedFileList
    }
    console.log(data);

  }
}
