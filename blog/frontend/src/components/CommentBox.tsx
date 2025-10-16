import React, { useState } from "react";
import { Textarea } from "@/components/ui/textarea";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog";

interface CommentBoxProps {
  placeholder?: string;
  onSubmit?: (commentText: string, file?: File | null) => Promise<void> | void;
  submittingText?: string;
  submitLabel?: string;
}

export const CommentBox: React.FC<CommentBoxProps> = ({
  placeholder = "Escreva um comentário...",
  onSubmit,
  submittingText = "Enviando...",
  submitLabel = "Comentar",
}) => {
  const [value, setValue] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [file, setFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);

  const handleSubmit = async () => {
    if (!value.trim() || submitting) return;
    try {
      setSubmitting(true);
      await onSubmit?.(value.trim(), file || undefined);
      setValue("");
      setFile(null);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <>
    <div className="space-y-3">
      <Textarea
        value={value}
        onChange={(e) => setValue(e.target.value)}
        placeholder={placeholder}
        className="min-h-[80px]"
        disabled={submitting}
      />
      <div className="flex items-center justify-between gap-3">
        <div className="flex items-center gap-3">
          <label className="cursor-pointer px-3 py-2 rounded-md border border-border bg-muted/30 text-sm text-foreground hover:bg-muted transition-smooth">
            Escolher arquivo
            <input
              type="file"
              onChange={(e) => setFile(e.target.files?.[0] || null)}
              className="hidden"
            />
          </label>
          {file ? (
            <div className="flex items-center gap-2">
              <Badge variant="outline" className="max-w-[220px] truncate">
                {file.name}
              </Badge>
              <Button
                type="button"
                variant="outline"
                size="sm"
                onClick={() => setPreviewUrl(URL.createObjectURL(file))}
              >
                Preview
              </Button>
              <Button
                type="button"
                variant="outline"
                size="sm"
                onClick={() => setFile(null)}
              >
                Remover
              </Button>
            </div>
          ) : null}
        </div>
        <Button
          onClick={handleSubmit}
          disabled={submitting || value.trim().length === 0}
          className="bg-primary-gradient hover:opacity-90 transition-smooth"
        >
          {submitting ? submittingText : submitLabel}
        </Button>
      </div>
    </div>
    <Dialog open={!!previewUrl} onOpenChange={(open) => { if (!open) { if (previewUrl) URL.revokeObjectURL(previewUrl); setPreviewUrl(null); } }}>
      <DialogContent className="max-w-3xl">
        <DialogHeader>
          <DialogTitle>Pré-visualização do arquivo</DialogTitle>
        </DialogHeader>
        <div className="w-full max-h-[70vh] overflow-auto">
          {previewUrl ? (
            <img src={previewUrl} alt="preview" className="max-w-full h-auto rounded-md" />
          ) : null}
        </div>
      </DialogContent>
    </Dialog>
    </>
  );
};

export default CommentBox;


